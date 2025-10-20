"""
Test de PP-StructureV3 para análisis de documentos estructurados
Extrae tablas, layout, fórmulas y más de documentos complejos
"""

from paddleocr import PPStructureV3
import json
import os
from pathlib import Path


def test_structure_basic():
    """Prueba básica de PP-StructureV3"""

    print("=" * 70)
    print("INICIANDO PP-StructureV3 - Análisis de Documentos Estructurados")
    print("=" * 70)

    # Inicializar PP-StructureV3
    print("\n[1/4] Inicializando PP-StructureV3...")
    print("   (Esto puede tardar un momento mientras descarga los modelos...)")
    print("   NOTA: Hay un bug conocido en el módulo de gráficos.")
    print("   Si falla, el OCR normal sigue siendo la mejor opción para tu caso.")

    # Usar configuración mínima para evitar el bug
    structure = PPStructureV3(
        device='cpu',
        lang='en'  # Usar inglés para evitar conflictos (puede reconocer español igual)
    )

    print("✓ PP-StructureV3 inicializado correctamente")

    # Ruta de imagen de prueba
    image_path = 'test_document.jpg'  # Cambia por tu imagen

    if not os.path.exists(image_path):
        print(f"\n⚠️  ADVERTENCIA: No se encontró '{image_path}'")
        print("   Coloca una imagen de documento en experimental/ocr/")
        print("   Ejemplos: factura, catálogo de producto, ficha técnica")
        return

    print(f"\n[2/4] Procesando imagen: {image_path}")
    print("   (Esto puede tardar 10-30 segundos en CPU...)")

    # Procesar imagen
    result = structure.predict(image_path)

    print(f"✓ Imagen procesada")

    # Analizar resultados
    print(f"\n[3/4] Analizando resultados...")

    documento_estructurado = {
        "archivo": image_path,
        "total_elementos": len(result),
        "elementos": []
    }

    # Estadísticas por tipo
    stats = {}

    for idx, elemento in enumerate(result):
        tipo = elemento.get('type', 'unknown')
        bbox = elemento.get('bbox', [])

        # Contar tipos
        stats[tipo] = stats.get(tipo, 0) + 1

        elemento_info = {
            "id": idx,
            "tipo": tipo,
            "bbox": bbox
        }

        # Extraer contenido según el tipo
        if tipo == 'text':
            # Texto normal
            elemento_info['texto'] = elemento.get('res', {}).get('text', '')
            elemento_info['confianza'] = elemento.get('res', {}).get('confidence', 0)

        elif tipo == 'title':
            # Título
            elemento_info['texto'] = elemento.get('res', {}).get('text', '')
            elemento_info['confianza'] = elemento.get('res', {}).get('confidence', 0)

        elif tipo == 'table':
            # Tabla estructurada
            table_html = elemento.get('res', {}).get('html', '')
            elemento_info['tabla_html'] = table_html
            elemento_info['tabla_celdas'] = elemento.get('res', {}).get('text', [])

        elif tipo == 'figure':
            # Imagen/Figura
            elemento_info['descripcion'] = 'Imagen detectada'

        elif tipo == 'formula':
            # Fórmula matemática
            elemento_info['formula'] = elemento.get('res', {}).get('text', '')

        documento_estructurado['elementos'].append(elemento_info)

    # Agregar estadísticas
    documento_estructurado['estadisticas'] = stats

    print(f"✓ Análisis completado")

    # Mostrar resumen
    print(f"\n[4/4] RESUMEN DE RESULTADOS:")
    print(f"   Total de elementos detectados: {len(result)}")
    print(f"\n   Desglose por tipo:")
    for tipo, cantidad in stats.items():
        print(f"      - {tipo.upper()}: {cantidad}")

    # Guardar resultados
    output_file = 'experimental/ocr/resultado_structure_v3.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documento_estructurado, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Resultados guardados en: {output_file}")

    # Mostrar algunos elementos de ejemplo
    print("\n" + "=" * 70)
    print("EJEMPLOS DE ELEMENTOS DETECTADOS:")
    print("=" * 70)

    for elemento in documento_estructurado['elementos'][:5]:  # Primeros 5
        print(f"\nElemento #{elemento['id']} - Tipo: {elemento['tipo'].upper()}")
        if 'texto' in elemento:
            texto = elemento['texto'][:100]  # Primeros 100 chars
            print(f"  Texto: {texto}...")
            print(f"  Confianza: {elemento.get('confianza', 0):.2f}")
        elif 'tabla_html' in elemento:
            print(f"  Tabla detectada (ver JSON para HTML completo)")
        print(f"  BBox: {elemento['bbox']}")

    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO ✓")
    print("=" * 70)


def test_structure_with_url():
    """Prueba PP-StructureV3 descargando imagen desde URL"""
    import httpx
    import tempfile
    from urllib.parse import urlparse

    print("=" * 70)
    print("PP-StructureV3 - Test con URL")
    print("=" * 70)

    # URL de ejemplo (cambiar por tu documento)
    url = "https://example.com/document.jpg"

    print(f"\n[1/5] Descargando imagen desde URL...")
    print(f"   {url}")

    try:
        # Descargar imagen
        response = httpx.get(url, timeout=30)
        response.raise_for_status()

        # Guardar temporalmente
        suffix = Path(urlparse(url).path).suffix or '.jpg'
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.write(response.content)
        temp_file.close()

        print(f"✓ Imagen descargada: {temp_file.name}")

        # Inicializar Structure
        print(f"\n[2/5] Inicializando PP-StructureV3...")
        structure = PPStructureV3(
            device='cpu',
            lang='en'
        )

        print(f"✓ Inicializado")

        # Procesar
        print(f"\n[3/5] Procesando documento...")
        result = structure.predict(temp_file.name)

        print(f"✓ Procesado: {len(result)} elementos detectados")

        # Limpiar archivo temporal
        os.unlink(temp_file.name)

        # Guardar resultado
        print(f"\n[4/5] Guardando resultados...")
        output = {
            "url": url,
            "total_elementos": len(result),
            "elementos": [
                {
                    "tipo": el.get('type'),
                    "bbox": el.get('bbox')
                }
                for el in result
            ]
        }

        with open('experimental/ocr/resultado_structure_url.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✓ Guardado en: experimental/ocr/resultado_structure_url.json")

        print(f"\n[5/5] Resumen:")
        tipos = {}
        for el in result:
            tipo = el.get('type', 'unknown')
            tipos[tipo] = tipos.get(tipo, 0) + 1

        for tipo, cant in tipos.items():
            print(f"   {tipo}: {cant}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    print("\n¿Qué test quieres ejecutar?")
    print("1. Test básico con imagen local")
    print("2. Test con URL")

    opcion = input("\nOpción (1 o 2): ").strip()

    if opcion == "1":
        test_structure_basic()
    elif opcion == "2":
        test_structure_with_url()
    else:
        print("Opción inválida. Ejecutando test básico...")
        test_structure_basic()