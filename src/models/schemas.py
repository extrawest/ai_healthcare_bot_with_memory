from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    user_message: str = Field(description="Chat message")
    user_id: str = Field(description="User ID")

