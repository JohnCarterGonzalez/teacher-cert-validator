from pydantic import BaseModel, Field

class ImageValidationRequest(BaseModel):
    model: str
    prompt: str
    images: list[str] = Field(..., description="List of base64-encoded image strings")

