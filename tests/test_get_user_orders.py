import requests
import allure
from urls import BASE_URL
from constants import ERROR_MESSAGE_UNAUTHORIZED


class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, created_user, ingredients):
        requests.post(
            f"{BASE_URL}/orders",
            headers={"Authorization": created_user["accessToken"]},
            json={"ingredients": ingredients[:2]}
        )

        response = requests.get(f"{BASE_URL}/orders", headers={"Authorization": created_user["accessToken"]})
        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True
        assert "orders" in body
        assert isinstance(body["orders"], list)

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_without_auth(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == ERROR_MESSAGE_UNAUTHORIZED
