import tkinter as tk
from tkinter import messagebox
from api_client_categorias import get_categorias, add_categoria, update_categoria, delete_categoria

def open_categorias_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Categorias")

    def refresh_list():
        listbox.delete(0, tk.END)
        for cat in get_categorias():
            listbox.insert(tk.END, f"{cat['cod_categoria']} - {cat['desc_categoria']}")

    def adicionar():
        data = {
            "cod_categoria": int(entry_codigo.get()),
            "desc_categoria": entry_descricao.get()
        }
        add_categoria(data)
        refresh_list()

    def atualizar():
        codigo = int(entry_codigo.get())
        data = {
            "cod_categoria": codigo,
            "desc_categoria": entry_descricao.get()
        }
        update_categoria(codigo, data)
        refresh_list()

    def deletar():
        codigo = int(entry_codigo.get())
        delete_categoria(codigo)
        refresh_list()

    # Labels e entradas
    tk.Label(window, text="Código:").grid(row=0, column=0)
    entry_codigo = tk.Entry(window)
    entry_codigo.grid(row=0, column=1)

    tk.Label(window, text="Descrição:").grid(row=1, column=0)
    entry_descricao = tk.Entry(window)
    entry_descricao.grid(row=1, column=1)

    # Botões
    tk.Button(window, text="Adicionar", command=adicionar).grid(row=2, column=0)
    tk.Button(window, text="Atualizar", command=atualizar).grid(row=2, column=1)
    tk.Button(window, text="Deletar", command=deletar).grid(row=2, column=2)

    # Lista
    listbox = tk.Listbox(window, width=80)
    listbox.grid(row=3, column=0, columnspan=3)

    refresh_list()
