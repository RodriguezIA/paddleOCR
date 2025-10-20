from fastapi import APIRouter, HTTPException
from src.schemas.ocr import OCRRequest, OCRResponse, OCRTextResult
from src.services.paddleOCR import ocr_service
from src.utils.image_downloader import download_image_from_url, cleanup_temp_file

router = APIRouter(prefix="/ocr", tags=["OCR"])


@router.post("/extract", response_model=OCRResponse)
async def extract_text_from_url(request: OCRRequest):
    """
    Extrae texto de una imagen desde URL usando OCR

    Args:
        request: OCRRequest con image_url y min_confidence opcional

    Returns:
        OCRResponse con los resultados del OCR
    """
    temp_file = None

    try:
        # Descargar imagen desde URL
        temp_file = await download_image_from_url(str(request.image_url))

        if not temp_file:
            raise HTTPException(
                status_code=400,
                detail="No se pudo descargar la imagen desde la URL"
            )

        # Realizar OCR
        results = ocr_service.extract_with_filter(
            temp_file,
            min_confidence=request.min_confidence
        )

        # Formatear respuesta
        ocr_results = [
            OCRTextResult(
                box=result["box"],
                text=result["text"],
                confidence=result["confidence"]
            )
            for result in results
        ]

        return OCRResponse(
            success=True,
            results=ocr_results,
            total_lines=len(ocr_results)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando OCR: {str(e)}"
        )
    finally:
        # Limpiar archivo temporal
        if temp_file:
            cleanup_temp_file(temp_file)


@router.post("/extract-text-only")
async def extract_text_only_from_url(request: OCRRequest):
    """
    Extrae solo el texto de una imagen (sin coordenadas ni confianza)

    Args:
        request: OCRRequest con image_url

    Returns:
        Texto extraído en formato simple
    """
    temp_file = None

    try:
        # Descargar imagen desde URL
        temp_file = await download_image_from_url(str(request.image_url))

        if not temp_file:
            raise HTTPException(
                status_code=400,
                detail="No se pudo descargar la imagen desde la URL"
            )

        # Realizar OCR y obtener solo texto
        text = ocr_service.extract_text_only(temp_file)

        return {
            "success": True,
            "text": text
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando OCR: {str(e)}"
        )
    finally:
        # Limpiar archivo temporal
        if temp_file:
            cleanup_temp_file(temp_file)