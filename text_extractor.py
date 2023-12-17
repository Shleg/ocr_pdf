import pytesseract


def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='rus')
    return text
