import json
from flask import url_for
from app import db
from app.models import User

from app.tests.test_base import BaseTestCase


class TestUserService(BaseTestCase):
    # some code...
    pass


def test_register(app):
    client = app.test_client()

    data = {
        "email": "mfsiddique11@gmail.com",
        "username": "mfsddique11",
        "password": "Faizan12345",
        "confirm_password": "Faizan12345"
    }

    resp = client.post(url_for('users.register'), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    print(resp.get_json('id'))
    u = User.query.get(resp.get_json('id'))
    u.confirm_id = True
    db.session.commit()
    assert resp.status_code == 201


def test_login(app):
    client = app.test_client()

    data = {
        "email": "mfsiddique11@gmail.com",
        "password": "Faizan12345"
    }

    resp = client.post(url_for('users.login'), data=json.dumps(data), headers={'Content-Type': 'application/json'})
    print(resp.data)

    assert resp.status_code == 200


def test_change_password(app):
    client = app.test_client()

    data = {
        "old_password": "Faizan12345",
        "new_password": "Faizan12345",
        "confirm_password": "Faizan12345",
    }

    resp = client.post(url_for('users.change_password'), data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    print(resp.data)
    assert resp.status_code == 201
