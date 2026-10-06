# AI Evaluation Support Prototype

A small human-in-the-loop prototype for turning unstructured interview notes into a consistent, reviewable evaluation structure.

## Why I built it

In assessment work, the same challenge repeats: behavioral evidence is rich and nuanced, but it still needs to be translated into a consistent rubric. I wanted a workflow that could make that translation faster and easier to audit without replacing the evaluator's judgment.

## What it does

1. Accepts written behavioral evidence from an interview.
2. Builds a strict LLM prompt around a configurable rubric.
3. Requests a structured JSON response for each dimension: suggested score, supporting evidence, counter-evidence, confidence, and rationale.
4. Runs validation checks before anything reaches the evaluator.
5. Keeps the final decision with the human reviewer.

## What broke in early iterations

The first prompt design was too sensitive to isolated phrases. A confident sentence could dominate the output even when the rest of the notes were mixed or weak.

I addressed that by requiring:
- evidence for every suggested score;
- explicit counter-evidence;
- a confidence level;
- a minimum-evidence rule;
- validation checks for missing dimensions, invalid score ranges, and unsupported outputs.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app works in **demo mode** with synthetic notes. If `OPENAI_API_KEY` is present, it can also call an LLM; otherwise it generates the prompt and lets you inspect the validation workflow.

## Privacy / scope

This public repo contains no real candidate information or proprietary assessment criteria. The included rubric and examples are generic and synthetic. It is a decision-support prototype only: it does not make hiring recommendations and the evaluator remains responsible for the final score.
