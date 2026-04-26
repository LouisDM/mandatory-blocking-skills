# MB-Protocol Verification Guide

> **Run this yourself. Get your own data.**

This guide walks you through a controlled experiment to verify whether MB-Protocol actually improves Agent execution reliability.

---

## What You'll Test

| Metric | Baseline (No MB-Protocol) | MB-Protocol |
|--------|--------------------------|-------------|
| **Comment Writeback Rate** | Agent writes feedback after task completion | Agent writes feedback after task completion |
| **Difference** | Standard step naming | `MANDATORY` + `BLOCKING` + Iron Rules |

**The ONLY difference between the two conditions is the prompt format.** Everything else (model, task, environment) stays identical.

---

## Prerequisites

- Python 3.8+
- An AI Agent that can run shell commands (Claude Code, Cursor, or any Agent with tool use)
- `curl` available

## Step 1: Start the Mock Application

```bash
cd mock-app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Verify it's running:
```bash
curl http://localhost:8000/health
# Expected: {"status":"ok","issues_count":0,"todos_count":0}
```

---

## Step 2: Run Baseline Experiment (Control Group)

### 2.1 Start the experiment runner

Open a new terminal:
```bash
cd experiments/verification-kit
python scripts/run-experiment.py --mode baseline --count 5 --output baseline-results.json
```

### 2.2 For each iteration, the script will:
1. Create a fresh Issue
2. Show you the Issue ID
3. Ask you to run the **baseline prompt** through your Agent

### 2.3 Copy the baseline prompt

Open `prompts/baseline-prompt.md` and copy its contents.

### 2.4 Run through your Agent

Paste the prompt into your Agent (replace `{ISSUE_ID}` with the actual ID shown by the script).

Let the Agent execute. Do NOT intervene.

### 2.5 Check results

After the Agent finishes, press Enter in the experiment script. It will automatically check whether the Agent wrote a comment to the Issue.

Repeat for 5 iterations.

---

## Step 3: Run MB-Protocol Experiment (Experimental Group)

### 3.1 Start the experiment

```bash
python scripts/run-experiment.py --mode mb-protocol --count 5 --output mb-protocol-results.json
```

### 3.2 Use the MB-Protocol prompt

Open `prompts/mb-protocol-prompt.md` and copy its contents.

### 3.3 Run through the SAME Agent

Use the same model, same settings, same everything. Only the prompt changes.

---

## Step 4: Collect Your Data

After both experiments complete, you'll have two JSON files:

```bash
cat baseline-results.json
cat mb-protocol-results.json
```

Each file contains:
```json
{
  "mode": "baseline",
  "count": 5,
  "results": [
    {
      "issue_id": "abc12345",
      "has_comments": true,
      "comment_count": 1,
      "issue_status": "done"
    }
  ],
  "summary": {
    "total": 5,
    "with_comments": 0,
    "without_comments": 5,
    "comment_rate": 0.0
  }
}
```

### Data Collection Template

Fill in this table with your results:

| # | Baseline (Comments?) | MB-Protocol (Comments?) |
|---|---------------------|------------------------|
| 1 | Yes / No | Yes / No |
| 2 | Yes / No | Yes / No |
| 3 | Yes / No | Yes / No |
| 4 | Yes / No | Yes / No |
| 5 | Yes / No | Yes / No |
| **Rate** | **X%** | **Y%** |

---

## Step 5: Share Your Results

We need data from diverse environments! Please share:

- **Platform**: Claude Code / Cursor / AutoGPT / Other
- **Model**: Claude 3.5 Sonnet / GPT-4 / Llama / etc.
- **Baseline Rate**: X%
- **MB-Protocol Rate**: Y%
- **Notes**: Any observations

Submit via:
- PR to `docs/EXPERIMENTS.md`
- Issue with your results
- Discussion post

---

## Expected Results (Based on Our Testing)

| Condition | Comment Rate | Notes |
|-----------|-------------|-------|
| **Baseline** | 0-20% | Agent often "forgets" to write comments under context pressure |
| **MB-Protocol** | 80-100% | BLOCKING format significantly improves compliance |

Your results may vary based on model, context length, and task complexity. That's exactly why we need more data!

---

## FAQ

### Q: Why manual instead of fully automated?

We want to test how **real Agents** behave, not scripted bots. Your actual Claude Code or Cursor session is the real test environment.

### Q: Can I run more than 5 iterations?

Absolutely. More iterations = more statistical power. 5 is the minimum.

### Q: What if my Agent doesn't support shell commands?

You can manually execute the curl commands the Agent would run, but this reduces the realism of the experiment.

### Q: Can I use a different mock app?

Yes, as long as it provides:
- Issue creation API
- Comment addition API
- Issue query API (to check if comments exist)

### Q: What about other metrics besides comment rate?

You can extend the experiment to measure:
- Deployment success rate (add a deploy step)
- Test pass rate (add test verification)
- Fix iteration count (add a bug to fix)

See `docs/EXPERIMENTS.md` for extended metrics.

---

## Quick Start (TL;DR)

```bash
# 1. Start mock app
cd mock-app && uvicorn main:app --port 8000

# 2. Run baseline (new terminal)
cd experiments/verification-kit
python scripts/run-experiment.py --mode baseline --count 5
# Follow prompts, copy baseline prompt to your Agent

# 3. Run MB-Protocol
python scripts/run-experiment.py --mode mb-protocol --count 5
# Follow prompts, copy MB-Protocol prompt to your Agent

# 4. Compare results
cat baseline-results.json
cat mb-protocol-results.json
```

**Let's build the evidence together.**
