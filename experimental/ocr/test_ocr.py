from paddleocr import PaddleOCR
import json

def test_ocr_local():
    """Prueba OCR con imagen local"""
    # Inicializar
    ocr = PaddleOCR(
        lang='es',
        device='cpu',
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False
    )

    # Cambiar por la ruta de tu imagen
    image_path = 'test_image.jpg'

    print(f"Procesando imagen: {image_path}")
    resultado = ocr.predict(image_path)

    documento_estructurado = {
        "tipo_documento": "test",
        "elementos": []
    }

    # Procesar resultados
    if resultado and len(resultado) > 0:
        page_result = resultado[0]
        dt_polys = page_result.get('dt_polys', [])

        # Buscar el texto en diferentes claves posibles
        rec_text = page_result.get('rec_text', [])
        if not rec_text:
            rec_text = page_result.get('rec_texts', [])

        rec_score = page_result.get('rec_score', [])
        if not rec_score:
            rec_score = page_result.get('rec_scores', [])

        print(f"Detecciones encontradas: {len(dt_polys)}")
        print(f"Textos encontrados: {len(rec_text)}")
        print(f"Scores encontrados: {len(rec_score)}")

        if rec_text:
            for idx in range(len(dt_polys)):
                bbox = dt_polys[idx]
                texto = rec_text[idx] if idx < len(rec_text) else ""
                confianza = rec_score[idx] if idx < len(rec_score) else 1.0

                if texto and texto.strip():
                    x_coords = [point[0] for point in bbox]
                    y_coords = [point[1] for point in bbox]
                    x1, x2 = int(min(x_coords)), int(max(x_coords))
                    y1, y2 = int(min(y_coords)), int(max(y_coords))

                    documento_estructurado["elementos"].append({
                        "id": idx,
                        "texto": texto.strip(),
                        "coordenadas": {
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2
                        },
                        "confianza": float(confianza)
                    })
        else:
            print("\n⚠️ No se encontró texto. Claves disponibles en el resultado:")
            print(list(page_result.keys()))

    # Guardar resultado
    with open('experimental/ocr/resultado.json', 'w', encoding='utf-8') as f:
        json.dump(documento_estructurado, f, ensure_ascii=False, indent=2)

    # Mostrar resultado
    print("\n" + "=" * 60)
    print(json.dumps(documento_estructurado, ensure_ascii=False, indent=2))
    print("=" * 60)
    print(f"\n✓ Procesado exitosamente.")
    print(f"  Total detecciones: {len(dt_polys)}")
    print(f"  Con texto válido: {len(documento_estructurado['elementos'])}")


if __name__ == "__main__":
    test_ocr_local()
