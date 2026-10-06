from scoring import validate_output, demo_result

RUBRIC = {
    "ownership": {},
    "adaptability": {},
    "collaboration": {},
    "self_regulation": {},
}


def test_demo_output_passes_schema():
    errors, _ = validate_output(demo_result(), RUBRIC)
    assert errors == []


def test_missing_dimension_is_flagged():
    result = demo_result()
    del result["ownership"]
    errors, _ = validate_output(result, RUBRIC)
    assert any("Missing dimension: ownership" in e for e in errors)
