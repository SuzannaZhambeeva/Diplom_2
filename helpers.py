def assert_successful_registration(response, payload):
    """Проверка успешной регистрации пользователя"""
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, body: {response.text}"
    body = response.json()
    assert body.get("success") is True
    assert "accessToken" in body and body["accessToken"].startswith("Bearer ")
    assert "refreshToken" in body
    assert body["user"]["email"] == payload["email"]
    assert body["user"]["name"] == payload["name"]


def assert_failed_registration(response, expected_message_substr=None):
    """Проверка неуспешной регистрации пользователя"""
    assert response.status_code == 403, f"Unexpected status: {response.status_code}, body: {response.text}"
    body = response.json()
    assert body.get("success") is False
    if expected_message_substr:
        assert expected_message_substr in body.get("message", ""), f"Message: {body.get('message')}"