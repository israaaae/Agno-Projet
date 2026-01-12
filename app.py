"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# src-layout support (so `import AgnoTest...` works under uvicorn)
SRC = ROOT / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

if os.environ.get("DEFAULT_MODEL_PROVIDER", "openai") == "openai" and not os.environ.get("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not set. Create a .env file or set the environment variable.")

from AgnoTest.core.base_orchestrator import AgentOSFactory  # noqa: E402
from AgnoTest.registry.teams import TEAMS  # noqa: E402

agent_os = AgentOSFactory(teams=[TEAMS["review_contract"]]).build()
app = agent_os.get_app()

"""
