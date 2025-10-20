import tempfile
import os
from typing import Optional
import httpx
from pathlib import Path
from urllib.parse import urlparse


async def download_image_from_url(url: str, timeout: int = 30) -> Optional[str]:
    """
    Descarga una imagen desde URL a un archivo temporal

    Args:
        url: URL de la imagen
        timeout: Timeout en segundos

    Returns:
        Path del archivo temporal o None si falla
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url)
            response.raise_for_status()

            # Extraer extensión del path de la URL (sin query params)
            parsed_url = urlparse(url)
            path_only = parsed_url.path
            suffix = Path(path_only).suffix

            # Si no hay extensión o no es válida, usar .jpg
            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
            if not suffix or suffix.lower() not in valid_extensions:
                suffix = '.jpg'

            # Crear archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            temp_file.write(response.content)
            temp_file.close()

            return temp_file.name

    except Exception as e:
        print(f"Error descargando imagen: {e}")
        return None


def cleanup_temp_file(file_path: str) -> None:
    """
    Elimina un archivo temporal

    Args:
        file_path: Ruta del archivo a eliminar
    """
    try:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f"Error eliminando archivo temporal: {e}")