import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db import Base, init_db
from main import app

# создаем тестовый клиент, который позволяет
# отправлять тестовые запросы в ASGI приложения
# по url заданным в app
client = TestClient(app)
password = 111111
username = 2


# dtoken['access_token']
# TODO найти способ решить проблему с парсингом получаемого токена для авторизации запроса

def test_login():
    token = client.post('/security/token', data={"username": username, "password": password})
    assert token.status_code == 200
    # pytest.set_trace()


# не проходит, хотя я получаю 401 в ответе
# возможно дело в том, что я не возвращаю ответ в случае не удачи
# а поднимаю исключение со статусом 401
def test_bad_login():
    emptytoken = client.post('/security/token', data={"username": 123, "password": 25})
    assert emptytoken.status_code == 401


def test_check_my_salary_for_unauth_user():
    response_without_token = client.get("my/salary")
    assert response_without_token.status_code == 401
    assert response_without_token.read() == b'{"detail":"Not authenticated"}'

    # pytest.set_trace()


def test_check_my_promotion_for_unauth_user():
    response_with_token = client.get("my/next_promotion")
    assert response_with_token.read() == b'{"detail":"Not authenticated"}'

# check_my_promotion
#
# check_salary_promotion
