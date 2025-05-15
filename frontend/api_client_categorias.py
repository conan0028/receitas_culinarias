import requests

API_URL = "http://127.0.0.1:8000"

def get_categorias():
    response = requests.get(f"{API_URL}/categorias")
    return response.json()

def add_categoria(data):
    response = requests.post(f"{API_URL}/categorias", json=data)
    return response.json()

def update_categoria(codigo, data):
    response = requests.put(f"{API_URL}/categorias/{codigo}", json=data)
    return response.json()

def delete_categoria(codigo):
    response = requests.delete(f"{API_URL}/categorias/{codigo}")
    return response.json()
