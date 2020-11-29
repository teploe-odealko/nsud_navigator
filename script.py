import requests

headers = {
    'Content-Type': 'application/json',
}

data = ' { "username": "elastic", "password": "jUU9t4jN7I8HbGIa7wudWB7F" }'

response = requests.post('https://63b59e3d9c4a4128ade4896a2e5f9811.us-central1.gcp.cloud.es.io:9243/0/api/v1/users/auth/_login', headers=headers, data=data, verify=False)
print(response.text)
