# import uvicorn
#
# if __name__ == "__main__":
#     # Executa o servidor FastAPI com recarregamento automático (ideal para desenvolvimento)
#     uvicorn.run(
#         "backend.main:app",  # Caminho para o objeto FastAPI
#         host="127.0.0.1",    # Endereço local
#         port=8000,           # Porta onde a aplicação vai rodar
#         reload=True          # Recarrega automaticamente ao detectar mudanças no código
#     )
import uvicorn
import threading
import subprocess
import sys
import os
from pathlib import Path

def run_backend():
    """Inicia o servidor FastAPI na porta 8000."""
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False  # Desative o reload para evitar conflitos com Tkinter
    )

def run_tkinter_app():
    """Inicia o frontend Tkinter."""
    frontend_dir = Path(__file__).parent / "frontend"  # Caminho para o frontend
    os.chdir(frontend_dir)

    # Comando para executar o Tkinter (ajuste conforme necessário)
    if sys.platform == "win32":
        subprocess.run(["python", "main_gui.py"], shell=True)
    else:
        subprocess.run(["python3", "main_gui.py"])

if __name__ == "__main__":
    # Inicia o FastAPI em uma thread separada (como daemon para fechar quando o Tkinter encerrar)
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # Inicia o Tkinter (bloqueia a thread principal)
    run_tkinter_app()
