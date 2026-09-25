# Backend — Лабораторная работа 1 (DevOps)

REST-бэкенд на Flask. Принимает текстовые данные с фронтенда и сохраняет их
в файл `data.txt` на сервере.

## Версии

| Тэг   | Содержимое                                              |
|-------|---------------------------------------------------------|
| v1.0  | `POST /api/data` — приём данных и запись в `data.txt`    |
| v2.0  | дополнительно `GET /api/data` — чтение содержимого `data.txt` |

## Установка и запуск

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Сервис запускается по адресу <http://127.0.0.1:5001>.

## Эндпоинты

### `GET /api/health`

Служебный эндпоинт для проверки доступности сервиса.

Ответ:

```json
{ "status": "ok", "version": "1.0" }
```

### `POST /api/data` (v1.0)

Принимает JSON с полем `text` и дописывает его в конец `data.txt`.

Запрос:

```json
{ "text": "Привет, сервер!" }
```

Успешный ответ (`201`):

```json
{ "status": "ok", "message": "Данные сохранены в data.txt", "records": 1 }
```

Если поле `text` пустое, возвращается `400`:

```json
{ "status": "error", "message": "Поле 'text' не должно быть пустым" }
```

### `GET /api/data` (v2.0)

Возвращает содержимое файла `data.txt`. Если файл ещё не создан, `content`
будет пустой строкой, а `count` — `0`.

Ответ:

```json
{ "status": "ok", "count": 2, "content": "Привет, сервер!\nВторая запись\n" }
```

## Проверка вручную

```bash
curl -X POST http://127.0.0.1:5001/api/data -H "Content-Type: application/json" -d "{\"text\": \"Привет\"}"
curl http://127.0.0.1:5001/api/data
```

## Структура проекта

```
backend/
├── app.py           # точка входа и обработчики запросов
├── requirements.txt # зависимости
├── data.txt         # файл с данными (создаётся во время работы, в git не отслеживается)
└── .gitignore
```
