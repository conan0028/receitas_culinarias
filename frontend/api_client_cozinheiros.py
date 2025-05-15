import requests
from requests.exceptions import RequestException

API_URL = "http://127.0.0.1:8000/cozinheiros"

def handle_request_errors(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)

            if response.status_code >= 400:
                error_detail = response.json().get('detail', response.text)
                return {"error": error_detail}

            return response.json() if response.status_code != 204 else {"message": "Operação realizada com sucesso"}

        except RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                error_detail = e.response.json().get('detail', e.response.text)
                return {"error": error_detail}
            return {"error": f"Erro de conexão: {str(e)}"}
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}
    return wrapper

@handle_request_errors
def get_cozinheiros():
    return requests.get(API_URL)

@handle_request_errors
def add_cozinheiro(data):
    return requests.post(API_URL, json=data)

@handle_request_errors
def update_cozinheiro(cpf, data):
    return requests.put(f"{API_URL}/{cpf}", json=data)

@handle_request_errors
def delete_cozinheiro(cpf):
    return requests.delete(f"{API_URL}/{cpf}")
