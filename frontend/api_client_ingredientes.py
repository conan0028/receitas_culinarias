import requests

API_URL = "http://127.0.0.1:8000"

def get_ingredientes():
    response = requests.get(f"{API_URL}/ingredientes")
    return response.json()

def add_ingrediente(data):
    response = requests.post(f"{API_URL}/ingredientes", json=data)
    return response.json()

def update_ingrediente(codigo, data):
    response = requests.put(f"{API_URL}/ingredientes/{codigo}", json=data)
    return response.json()

def delete_ingrediente(codigo):
    response = requests.delete(f"{API_URL}/ingredientes/{codigo}")
    return response.json()
