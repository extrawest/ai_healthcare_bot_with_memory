import uuid
import json
import chainlit as cl
import httpx
import sys
from pathlib import Path

from src.config.settings import settings
from src.utils import setup_logger

logger = setup_logger(__name__)

@cl.on_chat_start
async def on_chat_start():
    session_id = str(uuid.uuid4())
    user_id = f"user_{session_id[:8]}"

    cl.user_session.set("user_id", user_id)

    await cl.Message(content="Welcome to the AI Healthcare Support with Memory Configuration! How can I help you today?").send()

@cl.on_message
async def on_message(message: cl.Message) -> None:
    if message.author == "System":
        return

    user_id = cl.user_session.get("user_id")

    content = "🔄 Processing your request..."

    msg = cl.Message(content=content)
    await msg.send()

    async with httpx.AsyncClient() as client:
        url = f"http://{settings.host}:{settings.port}/chat/completions"
        payload = {
            "user_message": message.content,
            "user_id": user_id
        }

        headers = {
            "Accept": "text/event-stream",
            "Content-Type": "application/json"
        }

        logger.info(f"Making request to {url}")

        try:
            async with client.stream("POST", url, json=payload, headers=headers, timeout=60.0) as response:
                if response.status_code != 200:
                    error_text = await response.text()
                    msg.content = f"Error: {response.status_code} - {error_text}"
                    await msg.update()
                    return

                try:
                    content = ""
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue

                        if line == "[DONE]" or line == "data: [DONE]":
                            logger.info("Received DONE signal, ending stream")
                            break

                        json_str = line
                        if line.startswith("data: "):
                            json_str = line[6:].strip()
                        
                        if not json_str:
                            continue
                        
                        try:
                            data = json.loads(json_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    content += delta["content"]
                                    msg.content = content
                                    await msg.update()

                            logger.info(f"Received chunk: {json_str[:50]}...")
                        except json.JSONDecodeError as e:
                            logger.error(f"Error parsing JSON: {e}, line: {json_str[:50]}...")
                            continue
                except httpx.ReadError as e:
                    logger.warning(f"Stream reading error: {e}")
                    if content:
                        msg.content = content
                        await msg.update()
                    else:
                        msg.content = "Error: Connection closed unexpectedly"
                        await msg.update()
        except httpx.NetworkError as e:
            logger.error(f"Network error: {e}")
            msg.content = "Error: Network error"
            await msg.update()
        except httpx.TimeoutException as e:
            logger.error(f"Timeout exception: {e}")
            msg.content = "Error: Timeout exception"
            await msg.update()
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            msg.content = "Error: Unexpected error"
            await msg.update()


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))

    cl.run()