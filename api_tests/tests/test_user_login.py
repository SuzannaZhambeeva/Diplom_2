import requests
import allure


class TestUserLogin:

    @allure.title("Успешная авторизация пользователя")
    def test_successful_login(self, base_url, created_user):
        login_payload = {
            "email": created_user["email"],
            "password": created_user["password"]
        }
        response = requests.post(f"{base_url}/auth/login", json=login_payload)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body and body["accessToken"].startswith("Bearer ")
        assert body["user"]["email"] == login_payload["email"]

    @allure.title("Авторизация с неверным паролем")
    def test_login_with_wrong_password(self, base_url, created_user):
        login_payload = {
            "email": created_user["email"],
            "password": "wrongpassword"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_payload)

        assert response.status_code == 401
        body = response.json()
        assert body.get("success") is False
        assert "incorrect" in body.get("message", "").lower()
