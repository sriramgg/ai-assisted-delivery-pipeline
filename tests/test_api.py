import pytest
from fastapi.testclient import TestClient
from app.main import app, Task
from pydantic import ValidationError
@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv('DB_PATH',str(tmp_path/'test.db'))
    return TestClient(app)
def test_health(client): assert client.get('/health').json()=={'status':'ok'}
def test_crud(client):
    r=client.post('/api/tasks',json={'title':'Deploy'}); assert r.status_code==201
    i=r.json()['id']; assert len(client.get('/api/tasks').json())==1
    assert client.put(f'/api/tasks/{i}',json={'title':'Deploy','done':True}).json()['done']
    assert client.delete(f'/api/tasks/{i}').status_code==204
    assert client.get('/api/tasks').json()==[]
def test_invalid(client): assert client.post('/api/tasks',json={'title':''}).status_code==422
def test_missing(client): assert client.delete('/api/tasks/999').status_code==404
def test_model():
    with pytest.raises(ValidationError): Task(title='')
