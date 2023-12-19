import json

import cv2
from flask import Flask, request, jsonify , make_response
from pdf_converter import download_file, jpg_path, jpg_to_cv_image, grayscale, thresh, noise_removal
from text_extractor import extract_text_from_image
from pattern_finder import find_info_in_list
from service_func import delete_files_in_folder
from config import pattern_dict, ALLOWED_MIME_TYPES
import mimetypes

app = Flask(__name__)


def is_valid_pdf(file_path):
    file_mime, _ = mimetypes.guess_type(file_path)
    return file_mime in ALLOWED_MIME_TYPES


@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    try:
        # Получаем ссылку на PDF из тела запроса
        pdf_url = request.json.get('pdf_url')

        pdf_file_path = download_file(pdf_url)

        if not is_valid_pdf(pdf_file_path):
            raise ValueError('The file is not a PDF document')

        jpg_file_path = jpg_path(pdf_file_path)

        img_cv2 = jpg_to_cv_image(jpg_file_path)

        img_cv2_gray = grayscale(img_cv2)

        # img_bw = thresh(img_cv2_gray)
        # cv2.imwrite('downloaded_files/img_bw.jpg', img_bw)
        # display('downloaded_files/img_bw.jpg')

        # noise_img = noise_removal(img_bw)
        # cv2.imwrite('downloaded_files/noise_img.jpg', noise_img)
        # display('downloaded_files/noise_img.jpg')

        ocr_result_list = extract_text_from_image(img_cv2_gray)

        result = find_info_in_list(ocr_result_list, pattern_dict)

        # Преобразуем словарь в JSON-строку
        result_json = json.dumps(result, ensure_ascii=False)

        # Создаем объект ответа
        response = make_response(
            result_json.strip('%') or json.dumps({'result': 'Ничего не найдено'}, ensure_ascii=False))

        # Устанавливаем заголовки CORS
        response.headers.add('Access-Control-Allow-Origin', 'https://www.gcd-russia.com')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

        # Возвращаем ответ
        return response

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        # Удаляем файлы
        delete_files_in_folder('downloaded_files')


if __name__ == '__main__':
    app.run(debug=False, port=8000)
