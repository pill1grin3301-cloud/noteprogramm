# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from app.main import app  
from app.db.session import get_db
from app.models import Base

TEST_DATABASE_URL = "postgresql+psycopg://postgres:admin@test_db:5432/test_db"

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL, connect_args={"connect_timeout": 10})

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    def override_get_db():
        try:
            yield session
        finally:
            pass


    app.dependency_overrides[get_db] = override_get_db  
    yield session
    
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()


@pytest.fixture
def client(db_session):
    return TestClient(app)

@pytest.fixture
def created_task(client):
    """Создает задачу через API и возвращает данные созданной задачи"""
    response = client.post("/tasks/", json={"title": "test task", 'completed': False})
    return response.json() 

@pytest.fixture
def created_cat(client):
    """Создает категорию через API и возвращает данные созданной категории"""
    response = client.post("/categories/", json={"name": "test cat"})
    return response.json() 