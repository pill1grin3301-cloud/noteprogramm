

def test_read_all_tasks(client):
    response = client.get('/tasks/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task(client):
    response = client.post('/tasks/', json={'title': 'test task', 'completed': False})
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert response.json()['title'] == 'test task'

def test_update_task(client, created_task):
    task_id = created_task["id"]
    
    # Счастливый путь
    response = client.patch(f"/tasks/{task_id}", json={"title": "new task", "completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "new task"
    
    # Ошибка 404
    response = client.patch("/tasks/99999", json={"title": "new task"})
    assert response.status_code == 404

def test_delete_task(client, created_task):
    task_id = created_task["id"]

    # Счастливый путь
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Ошибка 404
    response = client.delete("/tasks/99999999")
    assert response.status_code == 404
