import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("YANDEX_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Проверьте файл .env")

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
HEADERS = {
    "Authorization": f"OAuth {TOKEN}",
    "Accept": "application/json"
}

@pytest.fixture
def auth_headers():
    """Возвращает заголовки для запросов."""
    return HEADERS

@pytest.fixture
def base_url():
    """Возвращает базовый URL."""
    return BASE_URL

@pytest.fixture
def create_test_folder(auth_headers, base_url):
    """
    Фикстура для тестов: создает папку перед тестом и удаляет после.
    Возвращает имя созданной папки.
    """
    folder_name = "Autotest_Setup_Folder"
    
    # Setup
    requests.put(f"{base_url}?path={folder_name}", headers=auth_headers)
    
    yield folder_name
    
    # Teardown
    teardown_response = requests.delete(f"{base_url}?path={folder_name}&permanently=true", headers=auth_headers)
    
    assert teardown_response.status_code in [202, 204, 404]