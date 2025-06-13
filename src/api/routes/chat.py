from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from src.dependencies.services import get_streaming_service
from src.models.schemas import LLMRequest
from src.services.streaming_service import StreamingService
from src.utils import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/completions")
async def chat_completions(
    request: LLMRequest,
    streaming_service: StreamingService = Depends(get_streaming_service)
) -> StreamingResponse:
    logger.info(f"Received chat completions request {request}")
    return await streaming_service.streaming_chat(request)
