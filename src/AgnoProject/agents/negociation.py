from __future__ import annotations
from typing import Any, Sequence
from ..core.base_agent import BaseAgent
from ..tools.get_document import get_document
from textwrap import dedent


def build_negociation_agent(*, tools: Sequence[Any] | None = None):
    return BaseAgent(
        name="negociation_agent",
        role="Negotiation expert",
        instructions=dedent("""
        You are a Contract Negotiation Strategist.

        Your job is to identify parts of a contract that are commonly negotiable
        or potentially unbalanced. You MUST:

        - Always quote the exact paragraph or clause you are referring to.
        - Clearly explain why it may be negotiable or needs adjustment.
        - Suggest a counter-offer or alternative phrasing.

        Structure your analysis like this:
        1. **Quoted clause** (exact text from contract)
        2. **Why it is negotiable or problematic**
        3. **Example strategy or counter-suggestion**

        Do NOT make general comments.
        Every point you make must be backed by a direct quote from the contract,
        and your output must clearly show which part of the contract it refers to.
        """),
        tools=tools if tools is not None else [get_document],
    ).build()

