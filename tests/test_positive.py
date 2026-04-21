import pytest
import requests

# Проверка имен: латиница, кириллица, с пробелом
VALID_NAMES = ["Lat_Name", "Русская_Папка", "Name with spaces"]

class TestPositiveAPI:
    
    def test_get_disk_info_success(self, auth_headers):
        """Проверка эндпоинта GET /v1/disk/ """
        url = "https://cloud-api.yandex.net/v1/disk/"
        response = requests.get(url, headers=auth_headers)
        assert response.status_code == 200
        assert "total_space" in response.json()

    @pytest.mark.parametrize("folder_name", VALID_NAMES)
    def test_put_create_folder_success(self, base_url, auth_headers, folder_name):
        """Проверка успешного создания папки (PUT) с разными валидными именами."""
        response = requests.put(f"{base_url}?path={folder_name}", headers=auth_headers)
        
        assert response.status_code == 201
        
        requests.delete(f"{base_url}?path={folder_name}&permanently=true", headers=auth_headers)

    def test_get_folder_info_success(self, base_url, auth_headers, create_test_folder):
        """Проверка получения информации о папке (GET) и валидация тела ответа."""
        folder_name = create_test_folder
        
        response = requests.get(f"{base_url}?path={folder_name}", headers=auth_headers)
        data = response.json()
        
        assert response.status_code == 200
        assert data["name"] == folder_name
        assert data["type"] == "dir"

    def test_post_copy_folder_success(self, base_url, auth_headers, create_test_folder):
        """Проверка копирования папки (POST)."""
        original_folder = create_test_folder
        copied_folder = original_folder + "_copy"
        
        copy_url = f"{base_url}/copy?from={original_folder}&path={copied_folder}"
        
        response = requests.post(copy_url, headers=auth_headers)
        assert response.status_code == 201
        
        requests.delete(f"{base_url}?path={copied_folder}&permanently=true", headers=auth_headers)

    def test_delete_folder_success(self, base_url, auth_headers):
        """Проверка полного цикла: создание -> удаление (DELETE) -> проверка отсутствия."""
        folder_name = "Folder_to_delete"
        
        requests.put(f"{base_url}?path={folder_name}", headers=auth_headers)
        
        response_delete = requests.delete(f"{base_url}?path={folder_name}&permanently=true", headers=auth_headers)
        assert response_delete.status_code in [202, 204]
        
        response_get = requests.get(f"{base_url}?path={folder_name}", headers=auth_headers)
        assert response_get.status_code == 404