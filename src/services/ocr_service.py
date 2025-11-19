from easyocr import Reader
import fitz
reader = Reader(['pt', 'en'])

def ocr_image(image_path):
    resultados = reader.readtext(image_path)
    texto_extraido = ""

    for (bbox, texto, probabilidade) in resultados:
        texto_extraido += texto + " "
    return texto_extraido

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = fitz.open(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        if len(text.strip()) < 50:  # Limite arbitrário
            for page in reader.pages:
                pix = page.get_pixmap()
                img_path = "temp_image.png"
                pix.save(img_path)
                text += ocr_image(img_path)
        return text

def extract_text_from_documents(document_path):
    if not document_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return extract_pdf_text(document_path)
    return ocr_image(document_path)
    