import json
import traceback

from typing import AsyncGenerator

from fastapi.responses import StreamingResponse
from fastapi import HTTPException

from src.agents.support_agent import AIHealthcareSupport
from src.models.schemas import LLMRequest
from src.utils import setup_logger
from src.utils.openai_mapper import create_streaming_openai_chunk

logger = setup_logger(__name__)


class StreamingService:
    def __init__(
        self,
        support_agent: AIHealthcareSupport
    ):
        self.support_agent = support_agent

    async def streaming_chat(self, request: LLMRequest) -> StreamingResponse:
        try:
            async def generate_stream() -> AsyncGenerator[str, None]:
                first_chunk = await create_streaming_openai_chunk(role="assistant")
                yield f"data: {json.dumps(first_chunk)}\n\n"

                response = self.support_agent.ask(question=request.user_message, user_id=request.user_id)
                
                if "messages" in response and response["messages"]:
                    full_content = response["messages"][0]

                    chunk_size = 10
                    
                    for i in range(0, len(full_content), chunk_size):
                        content_chunk = full_content[i:i+chunk_size]
                        chunk_data = await create_streaming_openai_chunk(content=content_chunk)
                        yield f"data: {json.dumps(chunk_data)}\n\n"

                final_chunk = await create_streaming_openai_chunk(finish_reason="stop")
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                }
            )
        except Exception as e:
            logger.error(f"Error in chat_completions: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=str(e))
