from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class OCRRequest(BaseModel):
    """Request schema para OCR"""
    image_url: HttpUrl
    min_confidence: Optional[float] = 0.5


class OCRTextResult(BaseModel):
    """Resultado de texto extraído"""
    box: List[List[float]]
    text: str
    confidence: float


class OCRResponse(BaseModel):
    """Response schema para OCR"""
    success: bool
    results: List[OCRTextResult]
    total_lines: int