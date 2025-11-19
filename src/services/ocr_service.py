from easyocr import Reader
import fitz
import os
from typing import Dict
from ..utils.file_utils import get_file_extension, cleanup_temp_file

class OCRService:
    def __init__(self):
        self.reader = Reader(['pt', 'en'])
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extrai texto de imagem usando EasyOCR"""
        try:
            results = self.reader.readtext(image_path)
            extracted_text = ""
            
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # Filtra resultados com baixa confiança
                    extracted_text += text + " "
            
            return extracted_text.strip()
        except Exception as e:
            raise Exception(f"Erro ao processar imagem: {str(e)}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrai texto de PDF usando PyMuPDF com fallback para OCR"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                page_text = page.get_text()
                text += page_text + "\n"
            
            # Se o texto extraído é muito pequeno, usa OCR
            if len(text.strip()) < 100:
                text = self._pdf_to_ocr(pdf_path)
            
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"Erro ao processar PDF: {str(e)}")
    
    def _pdf_to_ocr(self, pdf_path: str) -> str:
        """Converte PDF para imagens e aplica OCR"""
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img_path = f"temp_page_{page_num}.png"
            pix.save(img_path)
            
            try:
                page_text = self.extract_text_from_image(img_path)
                text += page_text + "\n"
            finally:
                cleanup_temp_file(img_path)
        
        doc.close()
        return text
    
    def extract_text(self, file_path: str) -> str:
        """Método principal para extrair texto de qualquer arquivo suportado"""
        extension = get_file_extension(file_path)
        
        if extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif extension in ['.jpg', '.jpeg', '.png']:
            return self.extract_text_from_image(file_path)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {extension}")
    
    def process_multiple_files(self, file_paths: Dict[str, str]) -> Dict[str, str]:
        """Processa múltiplos arquivos e retorna textos extraídos"""
        results = {}
        
        for filename, file_path in file_paths.items():
            try:
                text = self.extract_text(file_path)
                results[filename] = text
            except Exception as e:
                results[filename] = f"Erro ao processar arquivo: {str(e)}"
        
        return results

# Instância global do serviço
ocr_service = OCRService()
