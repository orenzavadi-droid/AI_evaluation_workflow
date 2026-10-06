import json
from pathlib import Path

SCORE_MIN = 1
SCORE_MAX = 5


def load_rubric(path="rubric.json"):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_prompt(notes: str, rubric: dict) -> str:
    dimensions = "\n".join(
        f"- {key}: {cfg['label']} — {cfg['description']}" for key, cfg in rubric.items()
    )
    return f"""You are assisting a trained evaluator. Do not make a hiring recommendation.
Use ONLY the behavioral evidence in the notes. Do not infer traits from demographics or protected characteristics.

For each dimension, return:
- suggested_score: integer 1-5
- supporting_evidence: list of exact behavioral observations from the notes
- counter_evidence: list of observations that point in the other direction
- confidence: low / medium / high
- rationale: one concise sentence

If evidence is insufficient, set confidence to low and explain what is missing.
Do not let a single phrase determine a score when the broader evidence is mixed.

DIMENSIONS
{dimensions}

NOTES
{notes}

Return valid JSON with one top-level key per dimension.
"""


def validate_output(result: dict, rubric: dict):
    errors = []
    warnings = []
    for key in rubric:
        if key not in result:
            errors.append(f"Missing dimension: {key}")
            continue
        item = result[key]
        score = item.get("suggested_score")
        if not isinstance(score, int) or not SCORE_MIN <= score <= SCORE_MAX:
            errors.append(f"{key}: score must be an integer from {SCORE_MIN} to {SCORE_MAX}")
        evidence = item.get("supporting_evidence") or []
        if not evidence:
            warnings.append(f"{key}: no supporting evidence — human review required")
        if len(evidence) < 2 and item.get("confidence") == "high":
            warnings.append(f"{key}: high confidence with limited evidence")
        if item.get("confidence") not in {"low", "medium", "high"}:
            errors.append(f"{key}: invalid confidence value")
        if "counter_evidence" not in item:
            warnings.append(f"{key}: counter-evidence field missing")
    return errors, warnings


def demo_result():
    return {
        "ownership": {
            "suggested_score": 4,
            "supporting_evidence": [
                "Reorganized tasks after a teammate dropped out",
                "Took responsibility for meeting the deadline"
            ],
            "counter_evidence": ["Initially tried to do too much alone"],
            "confidence": "high",
            "rationale": "Shows proactive responsibility with evidence of learning to delegate."
        },
        "adaptability": {
            "suggested_score": 4,
            "supporting_evidence": [
                "Changed the original plan to meet the deadline",
                "Adjusted delegation after supervisor feedback"
            ],
            "counter_evidence": [],
            "confidence": "high",
            "rationale": "Changed approach in response to constraints and feedback."
        },
        "collaboration": {
            "suggested_score": 4,
            "supporting_evidence": [
                "Asked teammate what they could realistically complete",
                "Checked assumptions before escalating conflict"
            ],
            "counter_evidence": [],
            "confidence": "high",
            "rationale": "Uses direct communication and collaborative problem solving."
        },
        "self_regulation": {
            "suggested_score": 3,
            "supporting_evidence": ["Continued working toward the deadline under pressure"],
            "counter_evidence": ["Reported becoming frustrated when taking on too much alone"],
            "confidence": "medium",
            "rationale": "Maintained functioning but described some difficulty regulating frustration."
        }
    }
