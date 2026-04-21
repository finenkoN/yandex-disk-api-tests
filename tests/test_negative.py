import pytest
import requests

# Неверные имена: пустое, пробелы, со слэшем (нет родительской папки)
INVALID_NAMES = [
    ("", 400), 
    ("Parent_Not_Exist/Child", 409)
]

class TestNegativeAPI:
    
    def test_unauthorized_request_returns_401(self, base_url):
        """Проверка безопасности: запрос без токена авторизации."""
        # Отправляем запрос вообще без заголовков
        response = requests.get(f"{base_url}?path=AnyFolder")
        
        assert response.status_code == 401 # Unauthorized

    @pytest.mark.parametrize("bad_name, expected_status", INVALID_NAMES)
    def test_create_folder_invalid_names_fails(self, base_url, auth_headers, bad_name, expected_status):
        """Проверка попытки создать папку с запрещенными именами."""
        response = requests.put(f"{base_url}?path={bad_name}", headers=auth_headers)
        
        assert response.status_code == expected_status

    def test_create_already_existing_folder_returns_409(self, base_url, auth_headers, create_test_folder):
        """Проверка бизнес-логики: попытка создать дубликат папки."""
        folder_name = create_test_folder # Фикстура уже создала эту папку
        
        # Пытаемся создать ее второй раз
        response = requests.put(f"{base_url}?path={folder_name}", headers=auth_headers)
        
        assert response.status_code == 409 # Conflict

    def test_get_non_existent_folder_returns_404(self, base_url, auth_headers):
        """Проверка запроса информации о несуществующем ресурсе."""
        folder_name = "Definitely_Does_Not_Exist_12345"
        
        response = requests.get(f"{base_url}?path={folder_name}", headers=auth_headers)
        
        assert response.status_code == 404 # Not Found