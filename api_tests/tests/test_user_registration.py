import requests
import allure
from helpers import assert_successful_registration, assert_failed_registration


class TestUserRegistration:

    @allure.title("Регистрация нового уникального пользователя")
    def test_create_unique_user(self, base_url, unique_email):
        payload = {
            "email": unique_email,
            "password": "password123",
            "name": "TestUser"
        }
        response = requests.post(f"{base_url}/auth/register", json=payload)
        assert_successful_registration(response, payload)

        token = response.json()["accessToken"]
        requests.delete(f"{base_url}/auth/user", headers={"Authorization": token})

    @allure.title("Регистрация уже существующего пользователя")
    def test_create_existing_user(self, base_url, unique_email):
        payload = {
            "email": unique_email,
            "password": "password123",
            "name": "Suzanna"
        }

        response_first = requests.post(f"{base_url}/auth/register", json=payload)
        assert_successful_registration(response_first, payload)
        token = response_first.json()["accessToken"]

        response_second = requests.post(f"{base_url}/auth/register", json=payload)
        assert_failed_registration(response_second, "already exists")

        requests.delete(f"{base_url}/auth/user", headers={"Authorization": token})

    @allure.title("Регистрация пользователя без обязательного поля (пароль)")
    def test_create_user_without_required_field(self, base_url, unique_email):
        payload = {
            "email": unique_email,
            "name": "NoPasswordUser"
        }
        response = requests.post(f"{base_url}/auth/register", json=payload)
        assert response.status_code == 403
        body = response.json()
        assert body.get("success") is False
        assert "required" in body.get("message", "").lower()
