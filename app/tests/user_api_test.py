import json

url = 'http://0.0.0.0:5000/'


def test_register(app):
    client = app.test_client()

    data = {
        "email": "mfsiddique11@gmail.com",
        "username": "mfsddique11",
        "password": "Faizan12345",
        "confirm_password": "Faizan12345"
    }

    resp = client.post('http://0.0.0.0:5000/user/register', data=json.dumps(data),
                       headers={'Content-Type': 'application/json'})
    assert resp.status_code == 201


def test_login(app):
    client = app.test_client()

    data = {
        "email": "mfsiddique11@gmail.com",
        "password": "Faizan"
    }

    resp = client.post(url + 'user/login', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200
