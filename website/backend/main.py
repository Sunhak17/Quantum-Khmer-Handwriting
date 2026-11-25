from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import config
import inference
from schemas import HealthResponse, PredictRequest, PredictResponse, QubitOption

app = FastAPI(title="Khmer Handwriting Recognition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}


@app.get("/api/qubit-options", response_model=list[QubitOption])
def qubit_options():
    return inference.available_qubit_options()


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        return inference.predict_drawing(req.image, req.n_qubits)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


FRONTEND_DIST = config.ROOT / "website" / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
