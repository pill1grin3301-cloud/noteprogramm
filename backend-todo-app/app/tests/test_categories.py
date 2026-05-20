from fastapi import status

def test_read_all_categories(client):
    """Тест Прочтения всех категорий,
       в любом случае должно быть -> 200"""
    
    response = client.get('/categories/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_category(client):
    """Тест Создания новой категории, должно вернуть -> 201"""

    response = client.post('/categories/', json={'name': 'test cat'})
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert response.json()['name'] == 'test cat'


def test_update_category(client, created_cat):
    """Тест Обновления категории,
       если категория существует ответ -> 200, 
       если такой нет -> 404"""
    category_id = created_cat["id"]
    
    # Счастливый путь
    response = client.patch(f"/categories/{category_id}", json={"name": "new cat"})
    assert response.status_code == 200
    assert response.json()["name"] == "new cat"
    
    # Ошибка 404
    response = client.patch("/categories/99999", json={"name": "new cat"})
    assert response.status_code == 404


def test_delete_category(client, created_cat):
    """Тест Удаления категории, 
       если категория существует ответ -> 204, 
       если такой нет -> 404"""
    
    category_id = created_cat["id"]

    # Счастливый путь
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 204

    # Ошибка 404
    response = client.delete("/categories/99999999")
    assert response.status_code == 404


def test_create_category_duplicate_name(client, created_cat):
    """Попытка создать категорию с существующим именем -> 409 Conflict"""
    response = client.post("/categories/", json={"name": created_cat["name"]})
    
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_update_category_dublicate_name(client, created_cat):
    # Создаем новую категорию
    cat2 = client.post('/categories/', json={'name': 'second category'}).json()

    # Пытаемся переименовать, имя новой в имя уже существующей
    response = client.patch(f"/categories/{cat2['id']}", json={'name': created_cat['name']})

    assert response.status_code == status.HTTP_409_CONFLICT
