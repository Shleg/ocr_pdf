import os
import cv2
import numpy as np
import requests
from urllib.parse import urlparse, unquote
from pdf2image import convert_from_path
from PIL import Image


def download_file(file_url, output_directory='downloaded_files'):
    # Парсим URL, чтобы получить имя файла
    parsed_url = urlparse(file_url)
    file_name = os.path.basename(unquote(parsed_url.path))

    # Создаем директорию для сохранения файлов, если её нет
    os.makedirs(output_directory, exist_ok=True)

    # Загружаем файл
    response = requests.get(file_url)
    file_path = os.path.join(output_directory, file_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path


def jpg_path(pdf_path, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(pdf_path)

    # Конвертируем первую страницу PDF в список изображений
    images = convert_from_path(pdf_path, first_page=0, last_page=1)

    if images:
        # Получаем первое изображение из списка
        first_image = images[0]

        # Получаем имя файла для сохранения (например, "document_first_page.png")
        output_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_first_page.jpg"
        output_path = os.path.join(output_dir, output_filename)

        # Сохраняем изображение в формате PNG
        first_image.save(output_path, "JPEG")

        return output_path
    else:
        print("Ошибка: Не удалось получить изображение из PDF.")
        return None


def jpg_to_cv_image(jpeg_path):
    pil_image = Image.open(jpeg_path)
    img_cv2 = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return img_cv2


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresh(image):
    thresh, im_bw = cv2.threshold(image, 150, 180, cv2.THRESH_BINARY)
    return im_bw


def noise_removal(image):
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image
