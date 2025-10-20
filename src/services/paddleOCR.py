from paddleocr import PaddleOCR
from typing import List, Dict, Any


class PaddleOCRService:
    """Servicio para realizar OCR usando PaddleOCR en CPU"""

    def __init__(
        self,
        lang: str = "en",
        device: str = "cpu"
    ):
        """
        Inicializa el servicio de OCR

        Args:
            lang: Idioma del modelo ('en', 'es', 'ch', etc.)
            device: Dispositivo a usar ('cpu' o 'gpu')
        """
        self.ocr = PaddleOCR(
            lang=lang,
            device=device,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )

    def extract_text(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Extrae texto de una imagen

        Args:
            image_path: Ruta de la imagen

        Returns:
            Lista de resultados con coordenadas y texto detectado
        """
        result = self.ocr.predict(image_path)

        if not result or len(result) == 0:
            return []

        # Formatear resultados
        formatted_results = []

        # El resultado es una lista, tomamos el primer elemento (primera página)
        page_result = result[0]

        # Obtener las cajas delimitadoras
        dt_polys = page_result.get('dt_polys', [])

        # Buscar el texto en diferentes claves posibles
        rec_texts = page_result.get('rec_text', [])
        if not rec_texts:
            rec_texts = page_result.get('rec_texts', [])

        # Buscar los scores
        rec_scores = page_result.get('rec_score', [])
        if not rec_scores:
            rec_scores = page_result.get('rec_scores', [])

        # Procesar cada detección
        for idx in range(len(dt_polys)):
            texto = rec_texts[idx] if idx < len(rec_texts) else ""
            score = rec_scores[idx] if idx < len(rec_scores) else 1.0
            bbox = dt_polys[idx]

            # Convertir numpy array a lista si es necesario
            if hasattr(bbox, 'tolist'):
                bbox = bbox.tolist()

            formatted_results.append({
                "box": bbox,
                "text": texto,
                "confidence": float(score)
            })

        return formatted_results

    def extract_text_only(self, image_path: str) -> str:
        """
        Extrae solo el texto de una imagen (sin coordenadas)

        Args:
            image_path: Ruta de la imagen

        Returns:
            Texto extraído concatenado
        """
        results = self.extract_text(image_path)
        return "\n".join([r["text"] for r in results])

    def extract_with_filter(
        self,
        image_path: str,
        min_confidence: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Extrae texto filtrando por confianza mínima

        Args:
            image_path: Ruta de la imagen
            min_confidence: Confianza mínima (0-1)

        Returns:
            Resultados filtrados por confianza
        """
        results = self.extract_text(image_path)
        return [r for r in results if r["confidence"] >= min_confidence]

    def batch_extract(
        self,
        image_paths: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Procesa múltiples imágenes

        Args:
            image_paths: Lista de rutas de imágenes

        Returns:
            Diccionario con resultados por imagen
        """
        results = {}
        for img_path in image_paths:
            results[img_path] = self.extract_text(img_path)
        return results


# Instancia global del servicio
ocr_service = PaddleOCRService()


# Funciones helper para uso directo
def extract_text_from_image(image_path: str) -> List[Dict[str, Any]]:
    """Extrae texto de una imagen usando la instancia global"""
    return ocr_service.extract_text(image_path)


def get_text_only(image_path: str) -> str:
    """Obtiene solo el texto de una imagen"""
    return ocr_service.extract_text_only(image_path)