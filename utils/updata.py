from threading import Lock
import json

user_data_lock = Lock()

user_data_template = {
    'yourBal': 8589934592
}

def load_user_data():
    with user_data_lock:
        try:
            with open('user_data.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

def save_user_data(user_data):
    with user_data_lock:
        with open('user_data.json', 'w') as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)


user_data_file_path = 'user_data.json'

# Проверяем, существует ли файл user_data.json и является ли он валидным JSON
try:
    with open(user_data_file_path, 'r') as file:
        user_data = json.load(file)
    print("ВСЕ ОТЛИЧНО")
except FileNotFoundError:
    # Если файл не найден, создаем новый с пустым объектом
    user_data = {}
    with open(user_data_file_path, 'w') as file:
        json.dump(user_data, file)
except json.JSONDecodeError:
    # Если файл не является валидным JSON, выводим сообщение об ошибке
    print(f"Файл {user_data_file_path} поврежден или не является валидным JSON.")
