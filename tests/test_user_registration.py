import requests
import allure
from helpers import assert_successful_registration
from urls import BASE_URL
from constants import ERROR_MESSAGE_USER_EXISTS, ERROR_MESSAGE_REQUIRED_FIELD


class TestUserRegistration:

    @allure.title("Регистрация нового уникального пользователя")
    def test_create_unique_user(self, unique_email):
        payload = {
            "email": unique_email,
            "password": "password123",
            "name": "TestUser"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert_successful_registration(response, payload)

        token = response.json()["accessToken"]
        requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self, unique_email):
        payload = {
            "email": unique_email,
            "password": "password123",
            "name": "Suzanna"
        }

        response_first = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert_successful_registration(response_first, payload)
        token = response_first.json()["accessToken"]

        response_second = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response_second.status_code == 403
        body = response_second.json()
        assert body.get("success") is False
        assert body.get("message") == ERROR_MESSAGE_USER_EXISTS

        requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})

    @allure.title("Регистрация пользователя без обязательного поля (пароль)")
    def test_create_user_without_required_field(self, unique_email):
        payload = {
            "email": unique_email,
            "name": "NoPasswordUser"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        assert response.status_code == 403
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == ERROR_MESSAGE_REQUIRED_FIELD
