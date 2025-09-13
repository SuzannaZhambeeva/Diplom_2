import pytest
import requests
import random
import string


@pytest.fixture
def base_url():
    return "https://stellarburgers.nomoreparties.site/api"


@pytest.fixture
def unique_email():
    """Генерирует уникальный email на каждый вызов"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{random_str}@mail.com"


@pytest.fixture
def created_user(base_url, unique_email):
    """
    Создаёт пользователя через /auth/register и возвращает данные:
    email, password, name, accessToken, refreshToken, user.
    После теста — удаляет пользователя через DELETE /auth/user.
    """
    payload = {
        "email": unique_email,
        "password": "password123",
        "name": "TestUser"
    }
    resp = requests.post(f"{base_url}/auth/register", json=payload)
    assert resp.status_code == 200, f"Register failed: {resp.text}"
    body = resp.json()
    token = body["accessToken"]

    user_data = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": token,
        "refreshToken": body.get("refreshToken"),
        "user": body.get("user", {})
    }

    yield user_data

    requests.delete(f"{base_url}/auth/user", headers={"Authorization": token})


@pytest.fixture
def ingredients(base_url):
    """Возвращает список валидных id ингредиентов"""
    response = requests.get(f"{base_url}/ingredients")
    assert response.status_code == 200, f"Ingredients failed: {response.text}"
    data = response.json()
    ids = [item["_id"] for item in data.get("data", [])]
    assert ids, "Список ингредиентов пуст — нечем создавать заказы"
    return ids