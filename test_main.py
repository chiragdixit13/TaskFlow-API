from fastapi.testclient import TestClient

from main import app

client=TestClient(app)



def test_health():
    response=client.get("/health")

    assert response.status_code==200
    assert response.json()=={"status":"healthy"}
    


def test_create_task():
    response=client.post("/tasks",json={"title":"Learn CI/CD"})  
    assert response.status_code==200
    assert response.json()["title"]=="Learn CI/CD"
    assert isinstance (response.json()["id"],int)

def test_get_task():
    created=client.post("/tasks",json={"title":"Learn CI/CD"})
    task_id=created.json()["id"]
    response=client.get(f"/tasks/{task_id}")
    assert response.status_code==200
    assert response.json()["title"]=="Learn CI/CD"


def test_update_task():
    created = client.post("/tasks", json={"title": "Learn Python"})
    task_id = created.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Learn CI/CD"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn CI/CD"
    assert response.json()["id"] == task_id



