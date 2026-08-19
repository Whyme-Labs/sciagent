from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import platform
import re
import time
from pathlib import Path
from typing import Iterable

import numpy as np
import torch
from huggingface_hub import model_info
from transformers import AutoModelForCausalLM, AutoTokenizer

Poly = tuple[tuple[int, int, int], ...]
ZERO: Poly = ()
ONE: Poly = ((0, 0, 1),)
X: Poly = ((1, 0, 1),)
Y: Poly = ((0, 1, 1),)
EVALUATOR_VERSION = "jumpbench-neural-v0.2-calibrated"


def from_dict(values: dict[tuple[int, int], int]) -> Poly:
    return tuple(sorted((i, j, int(c)) for (i, j), c in values.items() if int(c)))


def as_dict(poly: Poly) -> dict[tuple[int, int], int]:
    return {(i, j): c for i, j, c in poly}


def add(a: Poly, b: Poly) -> Poly:
    out = as_dict(a)
    for i, j, c in b:
        out[(i, j)] = out.get((i, j), 0) + c
    return from_dict(out)


def neg(a: Poly) -> Poly:
    return tuple((i, j, -c) for i, j, c in a)


def sub(a: Poly, b: Poly) -> Poly:
    return add(a, neg(b))


def mul(a: Poly, b: Poly) -> Poly:
    out: dict[tuple[int, int], int] = {}
    for ai, aj, ac in a:
        for bi, bj, bc in b:
            key = (ai + bi, aj + bj)
            out[key] = out.get(key, 0) + ac * bc
    return from_dict(out)


def power(a: Poly, exponent: int) -> Poly:
    result = ONE
    for _ in range(exponent):
        result = mul(result, a)
    return result


def value(poly: Poly, x: int, y: int) -> int:
    return int(sum(c * x**i * y**j for i, j, c in poly))


def ast_to_poly(node: ast.AST) -> Poly:
    if isinstance(node, ast.Expression):
        return ast_to_poly(node.body)
    if isinstance(node, ast.Name) and node.id in {"x", "y"}:
        return X if node.id == "x" else Y
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return ZERO if node.value == 0 else ((0, 0, int(node.value)),)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return neg(ast_to_poly(node.operand))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
        return ast_to_poly(node.operand)
    if isinstance(node, ast.BinOp):
        left = ast_to_poly(node.left)
        right = ast_to_poly(node.right)
        if isinstance(node.op, ast.Add):
            return add(left, right)
        if isinstance(node.op, ast.Sub):
            return sub(left, right)
        if isinstance(node.op, ast.Mult):
            return mul(left, right)
        if isinstance(node.op, ast.Pow) and isinstance(node.right, ast.Constant):
            exponent = int(node.right.value)
            if 0 <= exponent <= 6:
                return power(left, exponent)
    raise ValueError(ast.dump(node))


def parse_expression(text: str) -> Poly | None:
    """Parse the first submitted expression; later self-contradictions do not overwrite it."""
    normalized = text.replace("²", "**2").replace("^", "**").replace("−", "-").replace("×", "*")
    normalized = re.sub(r"\bxy\b", "x*y", normalized)
    candidates: list[str] = []
    for match in re.finditer(
        r"(?:Expression|Answer|f\s*\(\s*x\s*,\s*y\s*\))\s*[:=]\s*([^\n`]+)",
        normalized,
        re.I,
    ):
        candidates.append(match.group(1))
    candidates.extend(re.findall(r"```(?:python)?\s*([^`]+)```", normalized, re.I | re.S))
    candidates.extend(line for line in normalized.splitlines() if line.strip())
    candidates.append(normalized)
    seen: set[str] = set()
    for candidate in candidates:
        candidate = candidate.strip().strip("`$ .;,")
        if candidate in seen:
            continue
        seen.add(candidate)
        if "=" in candidate:
            candidate = candidate.split("=", 1)[-1].strip()
        candidate = re.sub(r"\b([0-9]+)\s*([xy])\b", r"\1*\2", candidate)
        candidate = candidate.split(" where ")[0].split(" because ")[0].strip()
        if not candidate or len(candidate) > 300:
            continue
        try:
            return ast_to_poly(ast.parse(candidate, mode="eval"))
        except Exception:
            continue
    return None


def evidence_text(rows: list[dict]) -> str:
    return "\n".join(f"f({row['x']},{row['y']})={row['value']}" for row in rows)


DEMONSTRATIONS = """Example 1
f(-1,-1)=-2
f(0,2)=2
f(2,1)=3
Expression: x + y

Example 2
f(-1,2)=-4
f(0,-1)=1
f(2,3)=3
Expression: x*y - y
"""


def discovery_prompt(rows: list[dict]) -> str:
    return (
        "Infer the exact integer polynomial from observations. Use only x, y, integer constants, +, -, and *. "
        "Write only one algebraically equivalent expression on the first line.\n\n"
        + DEMONSTRATIONS
        + "\nTarget\n"
        + evidence_text(rows)
        + "\nExpression:"
    )


def ranking_prompt(rows: list[dict]) -> str:
    return (
        "Infer the exact integer polynomial f from the observations. "
        "The continuation is one candidate expression.\n"
        + evidence_text(rows)
        + "\nExpression:"
    )


def ranking_null_prompt() -> str:
    return "Infer the exact integer polynomial f. The continuation is one candidate expression.\nExpression:"


def teach_prompt(expression: str) -> str:
    return (
        f"The exact rule has been taught: f(x,y) = {expression}.\n"
        "Write only one algebraically equivalent expression on the first line.\nExpression:"
    )


def teach_null_prompt() -> str:
    return "An exact polynomial rule has been taught. Write one algebraically equivalent rule.\nExpression:"


def query_prompt(record: dict) -> str:
    hypotheses = "\n".join(
        f"H{index + 1}: {candidate['expression']}"
        for index, candidate in enumerate(record["query_choice"]["candidates"])
    )
    options = "\n".join(
        f"evaluate at ({option['x']},{option['y']})"
        for option in record["query_choice"]["query_options"]
    )
    return (
        "Choose the single experiment whose possible outputs best distinguish these polynomial hypotheses.\n"
        + hypotheses
        + "\nAvailable experiments:\n"
        + options
        + "\nThe best experiment is evaluate at"
    )


def query_null_prompt() -> str:
    return "Choose one experiment. The best experiment is evaluate at"


def transfer_prompt(expression: str, x: int, y: int) -> str:
    renamed = expression.replace("x", "a").replace("y", "b")
    return (
        f"A reusable binary operator is M(a,b) = {renamed}. "
        f"Compute M(M({x},{y}),{y}). Write only the integer.\nAnswer:"
    )


def transfer_null_prompt() -> str:
    return "Compute the requested integer. Write only the integer.\nAnswer:"


def generate(model, tokenizer, prompt: str, max_new_tokens: int) -> str:
    encoded = tokenizer(prompt, return_tensors="pt")
    with torch.inference_mode():
        output = model.generate(
            **encoded,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            use_cache=True,
        )
    return tokenizer.decode(output[0, encoded["input_ids"].shape[1] :], skip_special_tokens=True)


def continuation_scores(model, tokenizer, prompt: str, continuations: list[str]) -> list[dict]:
    prompt_ids = tokenizer(prompt, add_special_tokens=True)["input_ids"]
    sequences: list[list[int]] = []
    prompt_lengths: list[int] = []
    for continuation in continuations:
        continuation_ids = tokenizer(" " + continuation, add_special_tokens=False)["input_ids"]
        sequences.append(prompt_ids + continuation_ids)
        prompt_lengths.append(len(prompt_ids))
    max_length = max(len(sequence) for sequence in sequences)
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id
    input_ids = torch.full((len(sequences), max_length), pad_id, dtype=torch.long)
    attention = torch.zeros_like(input_ids)
    for row, sequence in enumerate(sequences):
        input_ids[row, : len(sequence)] = torch.tensor(sequence)
        attention[row, : len(sequence)] = 1
    with torch.inference_mode():
        logits = model(input_ids=input_ids, attention_mask=attention).logits
        log_probs = torch.log_softmax(logits[:, :-1, :], dim=-1)
    outputs = []
    for row, sequence in enumerate(sequences):
        start = prompt_lengths[row]
        labels = input_ids[row, start : len(sequence)]
        positions = torch.arange(start - 1, len(sequence) - 1)
        token_log_probs = log_probs[row, positions, labels]
        outputs.append(
            {
                "continuation": continuations[row],
                "sum_logprob": float(token_log_probs.sum()),
                "mean_logprob": float(token_log_probs.mean()),
                "tokens": int(token_log_probs.numel()),
            }
        )
    return outputs


def calibrated_scores(model, tokenizer, prompt: str, continuations: list[str], null_prompt: str) -> list[dict]:
    conditional = continuation_scores(model, tokenizer, prompt, continuations)
    prior = continuation_scores(model, tokenizer, null_prompt, continuations)
    outputs = []
    for conditional_item, prior_item in zip(conditional, prior, strict=True):
        if conditional_item["tokens"] != prior_item["tokens"]:
            raise AssertionError("continuation tokenization changed across prompts")
        item = dict(conditional_item)
        item["null_mean_logprob"] = prior_item["mean_logprob"]
        item["calibrated_mean_logprob"] = conditional_item["mean_logprob"] - prior_item["mean_logprob"]
        item["calibrated_sum_logprob"] = conditional_item["sum_logprob"] - prior_item["sum_logprob"]
        outputs.append(item)
    return outputs


def rank_of_correct(scores: list[dict], correct_index: int, score_key: str = "calibrated_mean_logprob") -> int:
    ordering = sorted(range(len(scores)), key=lambda index: (-scores[index][score_key], index))
    return ordering.index(correct_index) + 1


def unique_numeric_options(correct: int, decoys: Iterable[int]) -> list[str]:
    values = [correct]
    for value_ in decoys:
        if value_ not in values:
            values.append(value_)
        if len(values) == 8:
            break
    delta = 1
    while len(values) < 8:
        for candidate in (correct + delta, correct - delta):
            if candidate not in values:
                values.append(candidate)
            if len(values) == 8:
                break
        delta += 1
    return [str(value_) for value_ in values]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--max-tasks", type=int, default=0)
    args = parser.parse_args()

    torch.set_num_threads(min(4, os.cpu_count() or 1))
    manifest_bytes = Path(args.manifest).read_bytes()
    manifest = json.loads(manifest_bytes)
    stop = args.start_index + args.max_tasks if args.max_tasks else None
    records = manifest["records"][args.start_index:stop]
    info = model_info(args.model, revision=args.revision)
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        revision=args.revision,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()
    started = time.time()
    rows = []

    for task_number, record in enumerate(records, start=1):
        target = tuple(tuple(int(v) for v in term) for term in record["target_polynomial"])
        options = record["candidate_options"]
        continuations = [option["expression"] for option in options]
        correct_index = next(
            index for index, option in enumerate(options)
            if option["pool_index"] == record["target_pool_index"]
        )
        row: dict = {
            "task_id": record["task_id"],
            "definition_cost": record["definition_cost"],
            "target_pool_index": record["target_pool_index"],
        }

        for condition in ("active", "random", "passive"):
            scores = calibrated_scores(
                model,
                tokenizer,
                ranking_prompt(record["evidence"][condition]),
                continuations,
                ranking_null_prompt(),
            )
            calibrated_rank = rank_of_correct(scores, correct_index)
            raw_rank = rank_of_correct(scores, correct_index, "mean_logprob")
            row[f"recognition_{condition}_rank"] = calibrated_rank
            row[f"recognition_{condition}_top1"] = int(calibrated_rank == 1)
            row[f"recognition_{condition}_raw_rank"] = raw_rank
            row[f"recognition_{condition}_scores"] = scores

        teach_scores = calibrated_scores(
            model, tokenizer, teach_prompt(record["target_expression"]), continuations, teach_null_prompt()
        )
        teach_rank = rank_of_correct(teach_scores, correct_index)
        row["teach_rank"] = teach_rank
        row["teach_top1"] = int(teach_rank == 1)
        row["teach_raw_rank"] = rank_of_correct(teach_scores, correct_index, "mean_logprob")
        row["teach_scores"] = teach_scores

        for condition in ("active", "passive"):
            generation = generate(model, tokenizer, discovery_prompt(record["evidence"][condition]), 48)
            parsed = parse_expression(generation)
            row[f"free_{condition}_generation"] = generation
            row[f"free_{condition}_parseable"] = int(parsed is not None)
            row[f"free_{condition}_exact"] = int(parsed == target)
            row[f"free_{condition}_parsed"] = None if parsed is None else [list(term) for term in parsed]

        echo_generation = generate(model, tokenizer, teach_prompt(record["target_expression"]), 48)
        echo_parsed = parse_expression(echo_generation)
        row["teach_echo_generation"] = echo_generation
        row["teach_echo_parseable"] = int(echo_parsed is not None)
        row["teach_echo_exact"] = int(echo_parsed == target)
        row["teach_echo_parsed"] = None if echo_parsed is None else [list(term) for term in echo_parsed]

        query_options = record["query_choice"]["query_options"]
        query_continuations = [f"({option['x']},{option['y']})" for option in query_options]
        query_scores = calibrated_scores(
            model, tokenizer, query_prompt(record), query_continuations, query_null_prompt()
        )
        selected_query_index = max(
            range(len(query_scores)), key=lambda index: query_scores[index]["calibrated_mean_logprob"]
        )
        selected_query = query_options[selected_query_index]
        correct_coordinates = {
            (option["x"], option["y"])
            for option in query_options
            if option["label"] in record["query_choice"]["correct_labels"]
        }
        row["query_selected_coordinate"] = [selected_query["x"], selected_query["y"]]
        row["query_correct"] = int((selected_query["x"], selected_query["y"]) in correct_coordinates)
        row["query_scores"] = query_scores

        x_value, y_value = 1, 2
        inner = value(target, x_value, y_value)
        correct_transfer = value(target, inner, y_value)
        decoys = []
        for option in options:
            parsed_option = parse_expression(option["expression"])
            if parsed_option is not None:
                decoys.append(value(parsed_option, value(parsed_option, x_value, y_value), y_value))
        numeric_options = unique_numeric_options(correct_transfer, decoys)
        transfer_scores = calibrated_scores(
            model,
            tokenizer,
            transfer_prompt(record["target_expression"], x_value, y_value),
            numeric_options,
            transfer_null_prompt(),
        )
        transfer_correct_index = numeric_options.index(str(correct_transfer))
        transfer_rank = rank_of_correct(transfer_scores, transfer_correct_index)
        row["transfer_rank"] = transfer_rank
        row["transfer_top1"] = int(transfer_rank == 1)
        row["transfer_raw_rank"] = rank_of_correct(transfer_scores, transfer_correct_index, "mean_logprob")
        row["transfer_correct_value"] = correct_transfer
        row["transfer_options"] = numeric_options
        row["transfer_scores"] = transfer_scores
        rows.append(row)
        print(args.model, task_number, "/", len(records), record["task_id"], flush=True)

    metrics = [
        "recognition_active_top1", "recognition_random_top1", "recognition_passive_top1",
        "teach_top1", "free_active_parseable", "free_active_exact", "free_passive_parseable",
        "free_passive_exact", "teach_echo_parseable", "teach_echo_exact", "query_correct", "transfer_top1",
    ]
    summary = {key: float(np.mean([row[key] for row in rows])) for key in metrics}
    output = {
        "benchmark": "JumpBench neural acquisition v0.2",
        "evaluator_version": EVALUATOR_VERSION,
        "scoring_rule": "conditional mean token log probability minus content-free mean token log probability",
        "model": args.model,
        "requested_revision": args.revision,
        "resolved_revision": info.sha,
        "parameter_count": sum(parameter.numel() for parameter in model.parameters()),
        "manifest_file_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "manifest_semantic_sha256": manifest.get("sha256_without_sha_field"),
        "start_index": args.start_index,
        "n_tasks": len(rows),
        "summary": summary,
        "rows": rows,
        "runtime_seconds": time.time() - started,
        "environment": {
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": __import__("transformers").__version__,
        },
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"model": args.model, "summary": summary, "runtime_seconds": output["runtime_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
