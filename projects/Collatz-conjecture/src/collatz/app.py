from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .core import collatz_scan_range, collatz_sequence
from .models import ScanItem, ScanRequest, ScanResponse, SequenceRequest, SequenceResponse

app = FastAPI(
    title="Collatz Conjecture API",
    description="Compute Collatz sequences and metadata.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/collatz/sequence", response_model=SequenceResponse)
def compute_sequence(payload: SequenceRequest) -> SequenceResponse:
    try:
        result = collatz_sequence(payload.start, max_steps=payload.max_steps)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return SequenceResponse(**result.as_dict())


@app.post("/collatz/scan", response_model=ScanResponse)
def scan_range(payload: ScanRequest) -> ScanResponse:
    try:
        items = collatz_scan_range(
            payload.start, payload.count, max_steps=payload.max_steps
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ScanResponse(data=[ScanItem(**item.as_dict()) for item in items])
