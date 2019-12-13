import pytest
import requests
import json

def test_register():
	url = 'http://0.0.0.0:5000/register'
	resp = requests.get(url)
	assert resp.status_code == 200


def test_register():
	url = 'http://0.0.0.0:5000/register'
	data = {
                  'email':'mfsiddique11@gmail.com',
                  'password':'Faizan'
               }

	resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        j=json.loads(resp.text)
	assert resp.status_code == 200
        assert j['email']=='mfsiddique11@gmail.com'


