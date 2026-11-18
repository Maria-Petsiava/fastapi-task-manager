from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_task_unauthorized():
    # Δοκιμάζουμε διαγραφή χωρίς token -> Πρέπει να απορριφθεί με 401!
    response = client.delete("/tasks/1")
    assert response.status_code == 401