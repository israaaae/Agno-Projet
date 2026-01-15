from dotenv import load_dotenv

load_dotenv()

from AgnoTest.core.base_orchestrator import AgentOSFactory
from AgnoTest.interfaces.whatsapp import WhatsappInterface
from AgnoTest.utils.logging import LOGGER

LOGGER.info("Starting...")


from AgnoTest.registry.teams import TEAMS

agent_os = AgentOSFactory(teams=[TEAMS["review_contract"]]).with_interface(WhatsappInterface(team=TEAMS["review_contract"])).build() # 3dna 2 functions f base_orchestrator (get_app) pour les app normales et with_interface pour les app avec interface (whatsapp)

if __name__ == "__main__":
    agent_os.serve(app="app_whatsapp:app", port=8000, reload=True)

