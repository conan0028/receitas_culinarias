import requests

API_URL = "http://127.0.0.1:8000"

def get_restaurantes():
    response = requests.get(f"{API_URL}/restaurantes")
    return response.json()

def add_restaurante(data):
    response = requests.post(f"{API_URL}/restaurantes", json=data)
    return response.json()

def update_restaurante(nome, data):
    response = requests.put(f"{API_URL}/restaurantes/{nome}", json=data)
    return response.json()

def delete_restaurante(nome):
    response = requests.delete(f"{API_URL}/restaurantes/{nome}")
    return response.json()
