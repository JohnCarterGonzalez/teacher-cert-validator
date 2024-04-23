"""
AI service that constructs a payload of a prompt and b64 encoded images. 
Sends that payload over to gpt-4-vision-preview and expects a response as JSON


TODO: At the moment there is little to no error handling:
    - what happens if the data is corrupted on transmission?
    - validation for the correctness of configuration variables
    - validation errors for models 
    - too large file sizes
    - unsupported file formats for images could cause the encoder to fail
    - api rate limits, api key expiration
    - logging, client friendly error messages, and monitoring of app
    - race conditions: make the application stateless (asyncio.Lock)
    - external api calls: state dependency
"""
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from services import image_encoder, openai_service

app = FastAPI()

@app.get("/ping", description="Are we cooking?")
async def pong():
    return { "status": "Oh we cooking"}

@app.post("/validate_images/")
async def validate_images(
    model: str = Form(...),
    prompt: str = Form(...),
    images: list[UploadFile] = File(...),
):
    encoded_images = [await image_encoder.encode_image_to_base64(image) for image in images]

    response_data = await openai_service.send_request_to_model(model, prompt, encoded_images)

    content = (
        response_data.get("choices", [{}])[0].get("message", {}).get("content", "No content available")
    )

    return JSONResponse(content={"content": content})

