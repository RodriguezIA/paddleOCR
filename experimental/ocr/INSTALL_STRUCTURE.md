# Instalación de PP-StructureV3

## ¿Qué es PP-StructureV3?

Es un pipeline avanzado que analiza la **estructura completa de documentos**:
- ✅ Detecta layout (títulos, párrafos, tablas, imágenes)
- ✅ Extrae tablas con su estructura
- ✅ Reconoce fórmulas matemáticas
- ✅ Identifica el orden de lectura
- ✅ Exporta a Markdown

## Requisitos

- Python 3.8+
- 4-8GB RAM disponible
- **CPU es suficiente** (no requiere GPU)

## Instalación (3 pasos)

### Paso 1: Instalar PaddlePaddle (Framework base)

**Para CPU:**

```bash
python -m pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

**Verifica la instalación:**

```bash
python -c "import paddle; print(paddle.__version__)"
```

Debería mostrar: `3.2.0`

### Paso 2: Instalar PaddleOCR con PP-StructureV3

**Opción A - Solo PP-StructureV3 (Recomendado para tu proyecto):**

```bash
pip install "paddleocr[doc-parser]"
```

Este grupo `doc-parser` incluye:
- ✅ PP-StructureV3 (análisis de documentos)
- ✅ Extracción de tablas
- ✅ Reconocimiento de fórmulas
- ✅ Detección de sellos
- ✅ Análisis de layout

**Opción B - Todas las funcionalidades (más pesado):**

```bash
pip install "paddleocr[all]"
```

Incluye: traducción de documentos, extracción de información, etc.

### Paso 3: Dependencias adicionales para nuestros tests

```bash
pip install httpx
```

### Verificar instalación completa

```bash
python -c "from paddleocr import PPStructureV3; print('✓ PP-StructureV3 instalado correctamente')"
```

## Resumen de comandos (copia y pega)

```bash
# 1. PaddlePaddle
python -m pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# 2. PaddleOCR con PP-StructureV3
pip install "paddleocr[doc-parser]"

# 3. Dependencias para tests
pip install httpx

# 4. Verificar
python -c "from paddleocr import PPStructureV3; print('✓ Instalación exitosa')"
```

## Uso Rápido

### Prueba con imagen local

1. Coloca una imagen de documento en `experimental/ocr/`
   - Puede ser: factura, catálogo, ficha técnica, tabla, etc.
   - Nombra la imagen: `test_document.jpg`

2. Ejecuta:
   ```bash
   python experimental/ocr/test_structure_v3.py
   ```

3. Selecciona opción `1` (test básico)

### Prueba con URL

1. Edita `test_structure_v3.py` y cambia la URL en la función `test_structure_with_url()`

2. Ejecuta:
   ```bash
   python experimental/ocr/test_structure_v3.py
   ```

3. Selecciona opción `2` (test con URL)

## Tiempos esperados en CPU

| Documento | Tamaño | Tiempo aproximado |
|-----------|--------|-------------------|
| Simple (1 página texto) | 1000x1500px | 5-10 segundos |
| Con tabla | 1000x1500px | 10-20 segundos |
| Complejo (múltiples tablas) | 1000x1500px | 20-40 segundos |

**Primera ejecución:** Tardará más porque descarga los modelos (~2-3GB)

## Grupos de dependencias disponibles

Según la documentación oficial:

| Grupo | Funcionalidad |
|-------|---------------|
| `doc-parser` | **PP-StructureV3** - Parsing de documentos, tablas, fórmulas |
| `ie` | PP-ChatOCRv4 - Extracción de información clave |
| `trans` | PP-DocTranslation - Traducción de documentos |
| `all` | Todas las funcionalidades anteriores |

## Optimizaciones para CPU

Si el procesamiento es muy lento, puedes:

1. **Desactivar módulos que no necesites**:
   ```python
   structure = PPStructureV3(
       device='cpu',
       lang='es',
       use_doc_orientation_classify=False,
       use_doc_unwarping=False,
       use_textline_orientation=False
   )
   ```

2. **Redimensionar imágenes antes de procesar**:
   ```python
   from PIL import Image

   img = Image.open('imagen.jpg')
   # Reducir a máximo 1500px de ancho
   img.thumbnail((1500, 1500))
   img.save('imagen_small.jpg')
   ```

## Comparación: OCR Normal vs PP-StructureV3

### Usa OCR Normal si necesitas:
- ✅ Solo extraer texto simple
- ✅ Respuesta rápida (< 2 segundos)
- ✅ Procesamiento en tiempo real
- ✅ Bajo consumo de memoria

### Usa PP-StructureV3 si necesitas:
- ✅ Extraer tablas estructuradas
- ✅ Identificar títulos, párrafos, secciones
- ✅ Procesar documentos complejos
- ✅ Entender layout del documento
- ⚠️ Toleras 10-30 segundos de procesamiento
- ⚠️ Tienes 4-8GB RAM disponible

## Troubleshooting

### Error: "No module named 'paddleocr'"
```bash
pip install "paddleocr[doc-parser]"
```

### Error: "DependencyError: PP-StructureV3 requires additional dependencies"
```bash
pip install "paddleocr[doc-parser]"
```

### Error al importar paddle
```bash
python -m pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
```

### Muy lento en CPU
- Reduce tamaño de imagen (max 1500px)
- Desactiva módulos opcionales (orientation, unwarping)
- Procesa de forma asíncrona en segundo plano

### Memoria insuficiente
- Cierra otras aplicaciones
- Procesa imágenes de menor resolución
- Procesa de una en una, no en batch

## Próximos pasos

Una vez que funcione el test, puedes:
1. Crear endpoint en la API para Structure
2. Comparar resultados con OCR normal
3. Decidir cuál usar según tu caso de uso

**Recomendación:** Empieza con OCR normal (que ya tienes) y usa PP-StructureV3 solo para documentos con tablas o layout complejo.
