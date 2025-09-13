import requests
import allure


class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, base_url, created_user, ingredients):
        requests.post(
            f"{base_url}/orders",
            headers={"Authorization": created_user["accessToken"]},
            json={"ingredients": ingredients[:2]}
        )

        response = requests.get(f"{base_url}/orders", headers={"Authorization": created_user["accessToken"]})
        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True
        assert "orders" in body
        assert isinstance(body["orders"], list)

    @allure.title("Получение заказов без авторизации")
    def test_get_orders_without_auth(self, base_url):
        response = requests.get(f"{base_url}/orders")
        assert response.status_code == 401
        body = response.json()
        assert body.get("success") is False
        assert "authoris" in body.get("message", "").lower()