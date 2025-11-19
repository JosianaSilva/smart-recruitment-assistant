import os
import tempfile
from typing import List, Dict
from fastapi import UploadFile
from .config import config

def validate_file(file: UploadFile) -> bool:
    """Valida se o arquivo é suportado"""
    return file.content_type in config.ALLOWED_FILE_TYPES

def validate_file_size(file: UploadFile) -> bool:
    """Valida o tamanho do arquivo"""
    file.file.seek(0, 2)  # Vai para o fim do arquivo
    size = file.file.tell()
    file.file.seek(0)  # Volta para o início
    return size <= config.MAX_FILE_SIZE

async def save_temp_file(file: UploadFile) -> str:
    """Salva arquivo temporariamente e retorna o caminho"""
    content = await file.read()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def cleanup_temp_file(file_path: str):
    """Remove arquivo temporário"""
    try:
        os.unlink(file_path)
    except OSError:
        pass

def get_file_extension(filename: str) -> str:
    """Retorna a extensão do arquivo"""
    return os.path.splitext(filename)[1].lower()