import requests
import allure
from urls import BASE_URL
from constants import ERROR_MESSAGE_UNAUTHORIZED


class TestUserUpdate:

    @allure.title("Изменение имени пользователя с авторизацией")
    def test_user_update_name_with_auth(self, created_user):
        new_name = "UpdatedUser"
        response = requests.patch(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": created_user["accessToken"]},
            json={"name": new_name}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["name"] == new_name

    @allure.title("Изменение email пользователя с авторизацией")
    def test_user_update_email_with_auth(self, created_user):
        new_email = created_user["email"].replace("@", "+upd@")
        response = requests.patch(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": created_user["accessToken"]},
            json={"email": new_email}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == new_email

        requests.patch(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": created_user["accessToken"]},
            json={"email": created_user["email"]}
        )

    @allure.title("Изменение пароля пользователя с авторизацией (проверка через логин)")
    def test_user_update_password_with_auth(self, created_user):
        new_password = "newPassword123!"

        resp_update = requests.patch(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": created_user["accessToken"]},
            json={"password": new_password}
        )
        assert resp_update.status_code == 200
        assert resp_update.json().get("success") is True

        resp_login = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": created_user["email"], "password": new_password}
        )
        assert resp_login.status_code == 200
        assert resp_login.json().get("success") is True

        requests.patch(
            f"{BASE_URL}/auth/user",
            headers={"Authorization": created_user["accessToken"]},
            json={"password": created_user["password"]}
        )

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_auth(self):
        response = requests.patch(f"{BASE_URL}/auth/user", json={"name": "UpdatedUser"})
        assert response.status_code == 401
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == ERROR_MESSAGE_UNAUTHORIZED
