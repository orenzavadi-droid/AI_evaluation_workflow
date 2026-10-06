import json
import os
from pathlib import Path
import streamlit as st
from scoring import load_rubric, build_prompt, validate_output, demo_result

st.set_page_config(page_title="AI Evaluation Support", page_icon="🧭", layout="wide")
st.title("AI Evaluation Support Prototype")
st.caption("Human-in-the-loop structure for turning behavioral notes into reviewable rubric evidence.")

rubric = load_rubric(Path(__file__).with_name("rubric.json"))
sample = Path(__file__).with_name("sample_notes.txt").read_text(encoding="utf-8")

notes = st.text_area("Behavioral notes", value=sample, height=210)

left, right = st.columns(2)
with left:
    if st.button("Build evaluation prompt", use_container_width=True):
        st.session_state["prompt"] = build_prompt(notes, rubric)
with right:
    if st.button("Run synthetic demo", use_container_width=True):
        st.session_state["result"] = demo_result()

if "prompt" in st.session_state:
    st.subheader("LLM prompt")
    st.code(st.session_state["prompt"], language="text")

if "result" in st.session_state:
    result = st.session_state["result"]
    errors, warnings = validate_output(result, rubric)
    st.subheader("Structured output")
    st.json(result)
    if errors:
        st.error("Validation errors: " + " | ".join(errors))
    else:
        st.success("Schema validation passed")
    for warning in warnings:
        st.warning(warning)

st.divider()
st.info("Public demo: synthetic notes + generic rubric only. No real candidate data. Final judgment remains with the evaluator.")
