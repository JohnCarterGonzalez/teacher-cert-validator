import httpx
from httpx import Timeout
from config import settings

async def send_request_to_model(model: str, prompt: str, images_base64: list[str]):
    url = settings.openai_url
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.api_key}"}

    content = [{"type": "text", "text": f"Prompt: {prompt}"}] + [
        {"type": "image_url", "image_url": {"url": image_base64, "detail": "high"}}
        for image_base64 in images_base64
    ]

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 300,
    }

    timeout = Timeout(30.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
    return response.json()

