import tkinter as tk
from tkinter import messagebox
from api_client_ingredientes import get_ingredientes, add_ingrediente, update_ingrediente, delete_ingrediente

def open_ingredientes_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Ingredientes")

    def refresh_list():
        listbox.delete(0, tk.END)
        for ing in get_ingredientes():
            listbox.insert(tk.END, f"{ing['cod_ingred']} - {ing['nome_ingred']}")

    def adicionar():
        data = {
            "cod_ingred": int(entry_codigo.get()),
            "nome_ingred": entry_nome.get()
        }
        add_ingrediente(data)
        refresh_list()

    def atualizar():
        codigo = int(entry_codigo.get())
        data = {
            "cod_ingred": codigo,
            "nome_ingred": entry_nome.get()
        }
        update_ingrediente(codigo, data)
        refresh_list()

    def deletar():
        codigo = int(entry_codigo.get())
        delete_ingrediente(codigo)
        refresh_list()

    # Labels e entradas
    tk.Label(window, text="Código:").grid(row=0, column=0)
    entry_codigo = tk.Entry(window)
    entry_codigo.grid(row=0, column=1)

    tk.Label(window, text="Nome:").grid(row=1, column=0)
    entry_nome = tk.Entry(window)
    entry_nome.grid(row=1, column=1)

    # Botões
    tk.Button(window, text="Adicionar", command=adicionar).grid(row=2, column=0)
    tk.Button(window, text="Atualizar", command=atualizar).grid(row=2, column=1)
    tk.Button(window, text="Deletar", command=deletar).grid(row=2, column=2)

    # Lista
    listbox = tk.Listbox(window, width=80)
    listbox.grid(row=3, column=0, columnspan=3)

    refresh_list()
