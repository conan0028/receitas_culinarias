import requests

API_URL = "http://127.0.0.1:8000"

def get_livros():
    response = requests.get(f"{API_URL}/livros")
    return response.json()

def add_livro(data):
    response = requests.post(f"{API_URL}/livros", json=data)
    return response.json()

def update_livro(titulo, data):
    response = requests.put(f"{API_URL}/livros/{titulo}", json=data)
    return response.json()

def delete_livro(titulo):
    response = requests.delete(f"{API_URL}/livros/{titulo}")
    return response.json()
