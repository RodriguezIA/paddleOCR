import pytest
from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_health_endpoint():
    """Prueba el endpoint de health"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_extract_text_only_success():
    """Prueba el endpoint extract-text-only con URL válida"""
    payload = {
        "image_url": "https://catinfog.com/wp-content/uploads/2019/02/ticket-palo-alto-1.jpg",
        "min_confidence": 0.5
    }

    response = client.post("/ocr/extract-text-only", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "text" in data
    assert data["success"] is True
    assert isinstance(data["text"], str)
    assert len(data["text"]) > 0


def test_extract_text_with_details():
    """Prueba el endpoint extract con detalles completos"""
    payload = {
        "image_url": "https://catinfog.com/wp-content/uploads/2019/02/ticket-palo-alto-1.jpg",
        "min_confidence": 0.3
    }

    response = client.post("/ocr/extract", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "results" in data
    assert "total_lines" in data
    assert data["success"] is True
    assert isinstance(data["results"], list)
    assert data["total_lines"] > 0

    # Verificar estructura de cada resultado
    if len(data["results"]) > 0:
        result = data["results"][0]
        assert "box" in result
        assert "text" in result
        assert "confidence" in result
        assert isinstance(result["box"], list)
        assert isinstance(result["text"], str)
        assert isinstance(result["confidence"], float)


def test_extract_invalid_url():
    """Prueba con URL inválida"""
    payload = {
        "image_url": "https://invalid-url-that-does-not-exist.com/image.jpg",
        "min_confidence": 0.5
    }

    response = client.post("/ocr/extract-text-only", json=payload)

    # Debería retornar error 400 o 500
    assert response.status_code in [400, 500]
    assert "detail" in response.json()


def test_extract_missing_url():
    """Prueba sin proporcionar URL"""
    payload = {
        "min_confidence": 0.5
    }

    response = client.post("/ocr/extract-text-only", json=payload)

    # Error de validación
    assert response.status_code == 422


def test_extract_with_different_confidence():
    """Prueba con diferentes niveles de confianza"""
    payload_low = {
        "image_url": "https://catinfog.com/wp-content/uploads/2019/02/ticket-palo-alto-1.jpg",
        "min_confidence": 0.1
    }

    payload_high = {
        "image_url": "https://catinfog.com/wp-content/uploads/2019/02/ticket-palo-alto-1.jpg",
        "min_confidence": 0.9
    }

    response_low = client.post("/ocr/extract", json=payload_low)
    response_high = client.post("/ocr/extract", json=payload_high)

    assert response_low.status_code == 200
    assert response_high.status_code == 200

    # Con confianza baja debería haber más resultados
    data_low = response_low.json()
    data_high = response_high.json()

    assert data_low["total_lines"] >= data_high["total_lines"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
