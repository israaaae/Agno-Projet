# app_streamlit.py
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from agno.media import File


ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Make `import AgnoTest...` work with src-layout when running `streamlit run`.
SRC = ROOT / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

st.sidebar.subheader("Auth")
api_key = st.sidebar.text_input("OPENAI_API_KEY", type="password", value=os.environ.get("OPENAI_API_KEY", ""))
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

if not os.environ.get("OPENAI_API_KEY"):
    st.sidebar.info("Add `OPENAI_API_KEY` (or create `.env`).")
    st.stop()


def get_team():
    # Import after key is set.
    from AgnoProject.registry.teams import TEAMS

    return TEAMS["review_contract"]


st.title("AI Contract Review System")
uploaded = st.file_uploader("Upload Contract", type=["pdf", "docx", "txt"])

if uploaded and st.button("Review", type="primary"):
    data = uploaded.getvalue()
    suffix = Path(uploaded.name).suffix if uploaded.name else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    with st.spinner("Reviewing..."):
        team = get_team()
        resp = team.run(
            input="Review this contract comprehensively.",
            files=[File(filepath=tmp_path, filename=uploaded.name, name=uploaded.name)],
        )
        st.markdown(resp.content)