import os
from flask import Flask, jsonify, request
from flask_cors import CORS

API_VERSION = "2.0"

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get("DATA_FILE", os.path.join(BASE_DIR, "data.txt"))


def count_records(lines) -> int:
    return sum(1 for line in lines if line.strip())


def read_data() -> str:
    if not os.path.exists(DATA_FILE):
        return ""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return file.read()


def find_records(content: str, query: str):
    lines = content.splitlines()
    if not query:
        return lines
    query = query.lower()
    return [line for line in lines if query in line.lower()]


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "version": API_VERSION})


@app.route("/api/data", methods=["POST"])
def save_data():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()

    if not text:
        return jsonify({
            "status": "error",
            "message": "Поле 'text' не должно быть пустым",
        }), 400

    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(text + "\n")

    content = read_data()
    return jsonify({
        "status": "ok",
        "message": "Данные сохранены в data.txt",
        "records": count_records(content.splitlines()),
    }), 201


@app.route("/api/data", methods=["GET"])
def get_data():
    content = read_data()
    query = request.args.get("query", "").strip()
    found = find_records(content, query)

    return jsonify({
        "status": "ok",
        "message": "Содержимое файла data.txt",
        "count": len(found),
        "total": count_records(content.splitlines()),
        "content": "\n".join(found),
    })


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5001"))
    debug = os.environ.get("DEBUG", "true").lower() in ("1", "true", "yes", "on")
    app.run(host=host, port=port, debug=debug)
