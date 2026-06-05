from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from model_loader import get_predictor
from preprocess import DISCLAIMER, preprocess_image, validate_upload

app = FastAPI(
    title="Melanoma Detection API",
    description="Educational skin lesion screening API. Not for medical diagnosis.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "melanoma-detector"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")

    try:
        validate_upload(file.content_type, len(content))
        tensor = preprocess_image(content)
        result = get_predictor().predict(tensor)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to process image.") from exc

    return {**result, "disclaimer": DISCLAIMER}
