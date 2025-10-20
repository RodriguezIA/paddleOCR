# Tests

Pruebas unitarias y de integración para la API.

## Estructura

- `test_ocr_endpoint.py` - Tests para los endpoints de OCR

## Ejecutar tests

### Todos los tests:
```bash
pytest
```

### Tests específicos:
```bash
pytest tests/test_ocr_endpoint.py -v
```

### Con cobertura:
```bash
pytest --cov=src tests/
```

## Dependencias

```bash
pip install pytest pytest-cov httpx
```
