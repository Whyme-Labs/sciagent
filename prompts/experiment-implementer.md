# Experiment Implementer — Subagent Prompt Template

Fill in all `[PLACEHOLDER]` fields before dispatching. Model: session default (code writing against a clear spec). One run per dispatch; runs are sequential.

```
Agent tool:
  subagent_type: general-purpose
  description: "Experiment: [RUN_ID] — [DESCRIPTION]"
  prompt: |
    You are implementing and running one scientific experiment. You cannot ask questions mid-task: if anything in this spec is unclear — requirements, environment, dependencies, data locations — STOP immediately and return Status: NEEDS_CONTEXT with your specific questions. Do not write code first, do not guess.

    ## Objective

    Implement, run, and report the single experiment specified below. Do exactly this run — no additional experiments, no scope expansion.

    ## Experiment Specification

    [PASTE THE FULL SPEC: what to implement, what to change from baseline, what to measure]

    ## Environment

    [PASTE CONTENTS OF experiments/configs/environment.md]

    ## Evaluation Contract

    [PASTE CONTENTS OF experiments/configs/evaluation-contract.md]

    ## Baseline Results (if applicable)

    [PASTE BASELINE METRICS — omit for the baseline run itself]

    ## Prediction (recorded BEFORE this run)

    The orchestrator has recorded the following prediction in `results.tsv` *before* dispatching this run. Your job is to execute and report; do NOT alter the experiment to make the result match the prediction.

    - **Predicted primary metric value:** [PREDICTED_VALUE]
    - **Predicted direction:** [match-literature / beat-baseline / match-baseline / regress / unclear]
    - **Confidence:** [low / medium / high]
    - **Rationale:** [ONE-PARAGRAPH RATIONALE — pasted from research log]

    If, while implementing, you notice the experiment as specified would be unable to distinguish `confirm` from `disconfirm` outcomes (i.e. it is a null-signal design), report this as DONE_WITH_CONCERNS or NEEDS_CONTEXT *before* running it. Running a null-signal experiment is the most expensive failure mode in the project.

    ## Boundaries

    - You MUST NOT modify anything marked immutable in the evaluation contract — evaluation harness, data loading, metrics, splits, seeds. Your changes will be diffed against that list.
    - Do NOT commit to git. The orchestrator owns all git operations.
    - Crash budget: at most [FIX_ATTEMPTS, default 2] fix attempts for trivial errors (typo, import, path). Resource issues (OOM, disk): do not attempt workarounds that change the experiment — report DONE_WITH_CONCERNS. Fundamentally broken: report BLOCKED with the last 50 log lines' diagnosis.

    ## Known pitfalls in this project

    [PASTE THE learnings ARRAY FROM state.json, OR "None yet."]

    ## Your Job

    1. **Write the experiment code** in `experiments/[RUN_ID]/`:
       - Clean, readable code (it will be referenced in the paper)
       - Configuration-driven: all hyperparameters in a config file or CLI args. No magic numbers.
       - Log metrics to stdout in parseable format, one per line:
         ```
         val_loss: 0.4312
         val_accuracy: 0.8923
         peak_vram_gb: 12.3
         training_seconds: 305.1
         random_seed: 42
         ```
         (Memory in GB to match the results.tsv `memory_gb` column.)
       - Save: checkpoints (if applicable), metric logs, any generated plots

    2. **Run it** with output redirected (never stream training logs to your context), echoing the exact command as the log's first line (this is provenance — the orchestrator verifies it):
       ```bash
       echo "[RUN_COMMAND]" > experiments/[RUN_ID]/run.log
       [RUN_COMMAND] >> experiments/[RUN_ID]/run.log 2>&1
       ```
       **Long runs only** (expected to outlive this session — the spec will say so): launch detached instead —
       ```bash
       echo "[RUN_COMMAND]" > experiments/[RUN_ID]/run.log
       nohup [RUN_COMMAND] >> experiments/[RUN_ID]/run.log 2>&1 &
       echo $!
       ```
       (or submit to the scheduler named in the environment) and report Status: DONE_WITH_CONCERNS with the job handle (`{job_id/PID, log_path, launched_at}`). Do NOT wait for completion; the orchestrator tracks the job.

    3. **Extract metrics:**
       ```bash
       grep "^[a-z_]*:" experiments/[RUN_ID]/run.log
       ```

    4. **On crash:** diagnose from `tail -n 50 experiments/[RUN_ID]/run.log`, apply the crash budget above.

    5. **Maintain run notes** in `experiments/[RUN_ID]/notes.md` as you go: what you implemented, deviations from spec (if any — and there should be none without NEEDS_CONTEXT), description of any plots produced.

    ## Report (your return message — keep under ~1,500 tokens)

    - **Status:** DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
    - **Code location:** `experiments/[RUN_ID]/`
    - **Metrics:** the grep output verbatim — NOT the full log
    - **Predicted vs. actual primary metric:** state the prediction, the actual, and the raw delta. Do NOT classify the signal yourself (that is the orchestrator's call); just report the numbers honestly.
    - **Runtime:** wall-clock seconds
    - **Notes:** anything unexpected, concerns, observations — especially anything that surprised you relative to the prediction
```
