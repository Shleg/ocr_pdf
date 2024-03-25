import cv2
import pytesseract

from config import WORD_LIST


# def extract_text_from_image(image):
#     text = pytesseract.image_to_string(image, lang='rus').strip().split('\n')
#     result = [str_item for str_item in text if len(str_item) > 4 ]
#     return result

def extract_text_from_image(image):
    # Извлекаем текст с изображения
    # custom_config = r'--psm 3'

    text = pytesseract.image_to_string(image, lang='rus').strip().split('\n')
    result = [str_item for str_item in text if len(str_item) > 4]

    count = 0
    # Проверяем наличие слова "диплом" в распознанном тексте
    while count < 3 and not any(word in ' '.join(result).lower() for word in WORD_LIST) and len(text) > 0:
        # Если слово "диплом" не найдено, поворачиваем изображение на 90 градусов по часовой стрелке
        rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

        # Извлекаем текст с повернутого изображения
        rotated_text = pytesseract.image_to_string(rotated_image, lang='rus').strip().split('\n')
        result = [str_item for str_item in rotated_text if len(str_item) > 4]

        count += 1
    return result
