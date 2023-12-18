import pytesseract


def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='rus').strip().split('\n')
    result = [str_item for str_item in text if len(str_item) > 7]
    return result
