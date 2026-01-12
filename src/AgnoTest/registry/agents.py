from ..agents.contract_structure import build_contract_structure_agent
from ..agents.legal_framework import build_legal_framework_agent
from ..agents.negociation import build_negociation_agent
from ..tools.get_document import get_document

def build_agents():
    structure = build_contract_structure_agent (tools=[get_document])
    legal = build_legal_framework_agent(tools=[get_document])
    negotiation = build_negociation_agent(tools=[get_document])
    return {
        "structure": structure,
        "legal": legal,
        "negotiation": negotiation,
    }


AGENTS = build_agents()

