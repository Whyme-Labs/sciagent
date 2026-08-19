from __future__ import annotations

import argparse
import json
import os
import platform
import time
from pathlib import Path

import torch
from huggingface_hub import model_info
from transformers import AutoModelForCausalLM, AutoTokenizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def generate(model, tokenizer, prompt: str, max_new_tokens: int = 96) -> str:
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
    continuation = output[0, encoded["input_ids"].shape[1] :]
    return tokenizer.decode(continuation, skip_special_tokens=True)


def main() -> None:
    args = parse_args()
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    started = time.time()
    info = model_info(args.model, revision=args.revision)
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    load_start = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        revision=args.revision,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.eval()
    load_seconds = time.time() - load_start

    prompts = {
        "arithmetic": "Complete the answer with only the result. 17 + 28 =",
        "repeat_expression": (
            "A newly discovered binary operator is defined by "
            "M(x,y)=x*x+x*y-y. Repeat only the expression after the equals sign.\n"
            "M(x,y)="
        ),
        "apply_taught_expression": (
            "Use the exact rule f(x,y)=x*x+x*y-y. Compute f(2,-1). "
            "Write only the integer answer.\nAnswer:"
        ),
        "infer_expression": (
            "An unknown polynomial f uses only x, y, integers, +, -, and *. "
            "It has these exact values:\n"
            "f(0,0)=0\n"
            "f(1,0)=1\n"
            "f(0,1)=-1\n"
            "f(1,1)=1\n"
            "f(2,-1)=3\n"
            "Write one expression for f(x,y), and nothing else.\n"
            "f(x,y)="
        ),
        "choose_candidate": (
            "An unknown function has exact values f(0,0)=0, f(1,0)=1, "
            "f(0,1)=-1, f(1,1)=1, and f(2,-1)=3. Choose the correct rule.\n"
            "A. x*x+x*y-y\n"
            "B. x*x-x*y+y\n"
            "C. x*y+x-y\n"
            "D. x*x+y*y-y\n"
            "Write only A, B, C, or D.\nAnswer:"
        ),
    }
    generations = {}
    for name, prompt in prompts.items():
        t0 = time.time()
        text = generate(model, tokenizer, prompt)
        generations[name] = {
            "prompt": prompt,
            "generation": text,
            "seconds": time.time() - t0,
        }
        print(f"[{name}] {text!r}", flush=True)

    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    payload = {
        "model": args.model,
        "requested_revision": args.revision,
        "resolved_revision": info.sha,
        "parameter_count": parameter_count,
        "model_type": getattr(model.config, "model_type", None),
        "architectures": getattr(model.config, "architectures", None),
        "transformers_version": __import__("transformers").__version__,
        "torch_version": torch.__version__,
        "python": platform.python_version(),
        "load_seconds": load_seconds,
        "total_seconds": time.time() - started,
        "generations": generations,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("model", "resolved_revision", "parameter_count", "load_seconds", "total_seconds")}, indent=2))


if __name__ == "__main__":
    main()
