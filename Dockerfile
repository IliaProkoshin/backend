# Образ бэкенда (Flask).
# База — официальный уменьшенный образ Python.
FROM python:3.12-slim

# Не создавать .pyc-файлы и не буферизовать вывод (логи сразу в docker logs).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочий каталог внутри контейнера.
WORKDIR /app

# Сначала зависимости — так слой кешируется и не пересобирается при правке кода.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем исходный код приложения.
COPY app.py .

# Сервис слушает 5001 внутри сети Docker (наружу порт не публикуется).
EXPOSE 5001

CMD ["python", "app.py"]
