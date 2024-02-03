# Используйте официальный образ Python
FROM python:3.9

# Установите рабочий каталог в контейнере
WORKDIR /usr/src/app

# Установите зависимости, включая OpenCV и Tesseract
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    tesseract-ocr \
    libtesseract-dev \
	poppler-utils \
	tesseract-ocr-rus \
 && rm -rf /var/lib/apt/lists/*

# Создайте и установите виртуальное окружение
# RUN python -m venv /venv
# ENV PATH="/venv/bin:$PATH"

# Установите зависимости Python
COPY ocr_pdf/requirements.txt .
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Скопируйте код приложения
COPY ocr_pdf/web_service.py .
COPY ocr_pdf/config.py .
COPY ocr_pdf/pattern_finder.py .
COPY ocr_pdf/text_extractor.py .
COPY ocr_pdf/pdf_converter.py .
COPY ocr_pdf/service_func.py .

# Копируем сертификаты
COPY /root/letsencrypt/certbot/conf/live/gcd.webtm.ru/fullchain.pem .
COPY /root/letsencrypt/certbot/conf/live/gcd.webtm.ru/privkey.pem .


# Укажите порт, на котором будет работать приложение
# EXPOSE 8000

# Запустите приложение при старте контейнера
# CMD ["gunicorn", "--preload", "-w", "4", "-b", "0.0.0.0:8000", "web_service:app", "--certfile", "fullchain.pem", "--keyfile", "privkey.pem", "-n", "web_service", "--reload"]
