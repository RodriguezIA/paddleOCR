import httpx
import tempfile
import os
from paddleocr import PaddleOCR
import json
from urllib.parse import urlparse
from pathlib import Path


def download_image(url: str) -> str:
    """Descarga imagen desde URL"""
    response = httpx.get(url, timeout=30)
    response.raise_for_status()

    # Extraer extensión
    parsed_url = urlparse(url)
    suffix = Path(parsed_url.path).suffix or '.jpg'

    # Crear archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(response.content)
    temp_file.close()

    return temp_file.name


def test_ocr_from_url():
    """Prueba OCR descargando imagen desde URL"""

    # Cambiar por tu URL
    image_url = "https://catinfog.com/wp-content/uploads/2019/02/ticket-palo-alto-1.jpg"

    temp_file = None
    try:
        print(f"Descargando imagen desde: {image_url}")
        temp_file = download_image(image_url)
        print(f"Imagen guardada temporalmente en: {temp_file}")

        # Inicializar OCR
        ocr = PaddleOCR(
            lang='es',
            device='cpu',
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )

        print("Procesando OCR...")
        resultado = ocr.predict(temp_file)

        # Procesar resultados
        if resultado and len(resultado) > 0:
            page_result = resultado[0]
            dt_polys = page_result.get('dt_polys', [])
            rec_text = page_result.get('rec_text', []) or page_result.get('rec_texts', [])
            rec_score = page_result.get('rec_score', []) or page_result.get('rec_scores', [])

            print(f"\nDetecciones encontradas: {len(dt_polys)}")
            print(f"Textos reconocidos: {len(rec_text)}")

            # Mostrar algunos textos
            print("\nPrimeros 10 textos reconocidos:")
            for i, texto in enumerate(rec_text[:10]):
                score = rec_score[i] if i < len(rec_score) else 0
                print(f"  {i+1}. {texto} (confianza: {score:.2f})")

            # Guardar resultado completo
            output = {
                "url": image_url,
                "total_detecciones": len(dt_polys),
                "textos": rec_text,
                "scores": [float(s) for s in rec_score]
            }

            with open('experimental/ocr/resultado_url.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            print(f"\n✓ Resultado guardado en: experimental/ocr/resultado_url.json")

    finally:
        # Limpiar archivo temporal
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
            print(f"\nArchivo temporal eliminado: {temp_file}")


if __name__ == "__main__":
    test_ocr_from_url()
