# Используйте официальный образ Python
FROM python:3.9

# Установите зависимости, включая OpenCV и Tesseract
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    tesseract-ocr \
    libtesseract-dev \
	poppler-utils \
	tesseract-ocr-rus \
 && rm -rf /var/lib/apt/lists/*

# Создайте и установите виртуальное окружение
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Установите зависимости Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Скопируйте код приложения
COPY web_service.py /app
COPY config.py /app
COPY pattern_finder.py /app
COPY text_extractor.py /app
COPY pdf_converter.py /app

WORKDIR /app

# Укажите порт, на котором будет работать приложение
EXPOSE 8000

# Запустите приложение при старте контейнера
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "web_service:app", "-n", "web_service"]
