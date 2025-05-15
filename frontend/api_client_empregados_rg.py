import requests

API_URL = "http://127.0.0.1:8000"

def get_empregados_rg():
    response = requests.get(f"{API_URL}/empregados_rg")
    return response.json()

def add_empregado_rg(data):
    response = requests.post(f"{API_URL}/empregados_rg", json=data)
    return response.json()

def update_empregado_rg(rg, data):
    response = requests.put(f"{API_URL}/empregados_rg/{rg}", json=data)
    return response.json()

def delete_empregado_rg(rg):
    response = requests.delete(f"{API_URL}/empregados_rg/{rg}")
    return response.json()
