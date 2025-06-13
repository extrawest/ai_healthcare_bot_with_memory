from src.agents.support_agent import AIHealthcareSupport
from src.services.streaming_service import StreamingService
from src.utils import setup_logger

logger = setup_logger(__name__)


def get_streaming_service() -> StreamingService:
    support_agent = AIHealthcareSupport()
    return StreamingService(
        support_agent=support_agent
    )
