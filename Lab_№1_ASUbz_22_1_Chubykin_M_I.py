import requests

# Базовый URL тестового сервера
BASE_URL = "https://jsonplaceholder.typicode.com"

print("=== ЗАДАНИЕ 1: GET-запрос ===")
# 1) GET - запрос: Получить список постов и вывести посты пользователей с четными id
response = requests.get(f"{BASE_URL}/posts")
if response.status_code == 200:
    posts = response.json()
    print("Посты пользователей с четными ID:")
    print("-" * 50)
    for post in posts:
        if post['userId'] % 2 == 0:  # Проверка на четный userId
            print(f"ID поста: {post['id']}")
            print(f"ID пользователя: {post['userId']}")
            print(f"Заголовок: {post['title']}")
            print(f"Тело: {post['body'][:100]}...")  # Выводим первые 100 символов тела поста
            print("-" * 50)
else:
    print(f"Ошибка при выполнении GET-запроса: {response.status_code}")

print("\n=== ЗАДАНИЕ 2: POST-запрос ===")
# 2) POST - запрос: Создать новый пост
new_post_data = {
    "userId": 1,
    "title": "Тестовый пост",
    "body": "Это тело тестового поста, созданного с помощью POST-запроса."
}

response = requests.post(f"{BASE_URL}/posts", json=new_post_data)
if response.status_code == 201:  # 201 Created - успешное создание ресурса
    created_post = response.json()
    print("Созданный пост (JSON):")
    print(created_post)
    # Сохраняем ID созданного поста для следующего задания
    created_post_id = created_post['id']
else:
    print(f"Ошибка при выполнении POST-запроса: {response.status_code}")
    # На случай ошибки, используем ID существующего поста для демонстрации PUT-запроса
    created_post_id = 1
    print("Используем ID=1 для демонстрации PUT-запроса")

print("\n=== ЗАДАНИЕ 3: PUT-запрос ===")
# 3) PUT - запрос: Обновить ранее созданный пост
updated_post_data = {
    "userId": 1,
    "id": created_post_id,  # Используем ID созданного поста
    "title": "Обновлённый пост",
    "body": "Это обновленное тело поста, измененное с помощью PUT-запроса."
}

response = requests.put(f"{BASE_URL}/posts/{created_post_id}", json=updated_post_data)
if response.status_code == 200:
    updated_post = response.json()
    print("Обновленный пост (JSON):")
    print(updated_post)
else:
    print(f"Ошибка при выполнении PUT-запроса: {response.status_code}")