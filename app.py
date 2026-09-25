"""Backend версии 1.0.

Принимает текстовые данные, отправленные с фронтенда, и сохраняет их
в текстовый файл data.txt на сервере.
"""

import os

from flask import Flask, jsonify, request
from flask_cors import CORS

API_VERSION = "1.0"

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")


def count_records() -> int:
    """Вернуть количество непустых записей, сохранённых в data.txt."""
    if not os.path.exists(DATA_FILE):
        return 0
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return sum(1 for line in file if line.strip())


@app.route("/api/health", methods=["GET"])
def health():
    """Проверка доступности сервиса."""
    return jsonify({"status": "ok", "version": API_VERSION})


@app.route("/api/data", methods=["POST"])
def save_data():
    """Принять данные с фронтенда и дописать их в data.txt."""
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()

    if not text:
        return jsonify({
            "status": "error",
            "message": "Поле 'text' не должно быть пустым",
        }), 400

    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(text + "\n")

    return jsonify({
        "status": "ok",
        "message": "Данные сохранены в data.txt",
        "records": count_records(),
    }), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
