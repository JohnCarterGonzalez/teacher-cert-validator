import base64
from fastapi import UploadFile

async def encode_image_to_base64(image_file: UploadFile) -> str:
    image_content = await image_file.read()
    base64_encoded = base64.b64encode(image_content).decode("utf-8")
    return f"data:image/jpeg;base64,{base64_encoded}"

