# Experiment Implementer — Subagent Prompt Template

Use this template when dispatching an experiment implementer subagent. Fill in all `[PLACEHOLDER]` fields before dispatching.

```
Agent tool:
  subagent_type: general-purpose
  model: sonnet
  description: "Experiment: [RUN_ID] — [DESCRIPTION]"
  prompt: |
    You are implementing and running a scientific experiment.

    ## Experiment Specification

    [PASTE THE FULL EXPERIMENT SPEC: what to implement, what to change from baseline, what to measure]

    ## Environment

    [PASTE CONTENTS OF experiments/configs/environment.md]

    ## Evaluation Contract

    [PASTE CONTENTS OF experiments/configs/evaluation-contract.md]

    You MUST NOT modify anything marked as immutable in the evaluation contract.

    ## Baseline Results (if applicable)

    [PASTE BASELINE METRICS — omit for the baseline run itself]

    ## Before You Begin

    If you have questions about:
    - The experiment requirements
    - The environment setup
    - Dependencies or data locations
    - Anything unclear

    **Ask now.** Do not guess.

    ## Your Job

    1. **Write the experiment code** in `experiments/[RUN_ID]/`:
       - Clean, readable code (this will be referenced in the paper)
       - Configuration-driven: all hyperparameters in a config file or CLI args. No magic numbers.
       - Must log these metrics to stdout in parseable format:
         ```
         metric_name: value
         ```
         Example:
         ```
         val_loss: 0.4312
         val_accuracy: 0.8923
         peak_vram_mb: 12543.2
         training_seconds: 305.1
         random_seed: 42
         ```
       - Must save: checkpoints (if applicable), metric logs, any generated plots

    2. **Run the experiment** using context management:
       ```bash
       [RUN_COMMAND] > experiments/[RUN_ID]/run.log 2>&1
       ```

    3. **Extract and report metrics:**
       ```bash
       grep "^[a-z_]*:" experiments/[RUN_ID]/run.log
       ```

    4. **If it crashes:**
       - Read the last 50 lines: `tail -n 50 experiments/[RUN_ID]/run.log`
       - If trivial fix (typo, import, path): fix and re-run (max 2-3 attempts)
       - If resource issue (OOM): report as DONE_WITH_CONCERNS
       - If fundamentally broken: report as BLOCKED

    5. **Commit your code** (NOT the log file or data):
       ```bash
       git add experiments/[RUN_ID]/
       git commit -m "research: exp [RUN_ID] — [DESCRIPTION]"
       ```

    ## Report

    - **Status:** DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
    - **Code location:** `experiments/[RUN_ID]/`
    - **Metrics:** (paste the grep output — NOT the full log)
    - **Runtime:** wall-clock seconds
    - **Notes:** anything unexpected, concerns, observations
```
