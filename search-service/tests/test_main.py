import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app, get_es_client

# --- Fixture pentru Clientul de Test ---
@pytest.fixture(scope="function")
def client():
    yield TestClient(app)
    # Curățăm suprascrierile după fiecare test
    app.dependency_overrides.clear()

# --- Teste ---

def test_search_products_success(client, mocker):
    """
    Testează o căutare reușită, simulând un răspuns de la Elasticsearch.
    """
    # 1. Cream un obiect mock care va simula clientul Elasticsearch
    mock_es_client = MagicMock()
    
    # 2. Definim răspunsul fals pe care trebuie să-l returneze la apelul metodei `search`
    mock_es_client.search.return_value = {
        "hits": {
            "hits": [
                {"_source": {"id": 1, "name": "Test Laptop", "description": "Rapid"}},
                {"_source": {"id": 2, "name": "Alt Laptop", "description": "Usor"}}
            ]
        }
    }
    
    # 3. Suprascriem dependența `get_es_client` pentru a returna clientul nostru simulat
    app.dependency_overrides[get_es_client] = lambda: mock_es_client
    
    # 4. Facem request-ul la API
    response = client.get("/search?q=laptop")
    
    # 5. Verificăm rezultatele
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Laptop"
    
    # 6. Verificăm că metoda `search` a clientului simulat a fost apelată corect
    mock_es_client.search.assert_called_once()


def test_search_products_empty_query(client, mocker):
    """
    Testează căutarea cu un query gol, care ar trebui să returneze o listă goală.
    """
    mock_es_client = MagicMock()
    app.dependency_overrides[get_es_client] = lambda: mock_es_client
    
    response = client.get("/search?q=")
    
    assert response.status_code == 200
    assert response.json() == []
    
    # Verificăm că metoda `search` a clientului simulat NU a fost apelată
    mock_es_client.search.assert_not_called()

def test_search_elasticsearch_error(client, mocker):
    """
    Testează cum se comportă serviciul dacă Elasticsearch returnează o eroare.
    """
    mock_es_client = MagicMock()
    # Simulăm o excepție la apelul metodei `search`
    mock_es_client.search.side_effect = Exception("Connection error")
    
    app.dependency_overrides[get_es_client] = lambda: mock_es_client
    
    response = client.get("/search?q=orice")
    
    # În `main.py`, am ales să returnăm un dicționar cu o eroare, fără un status code specific
    assert response.status_code == 200 
    assert response.json() == {"error": "Search failed"}