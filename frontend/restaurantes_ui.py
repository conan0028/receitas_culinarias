import tkinter as tk
from tkinter import messagebox
from api_client_restaurantes import get_restaurantes, add_restaurante, update_restaurante, delete_restaurante

def open_restaurantes_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Restaurantes")

    def refresh_list():
        listbox.delete(0, tk.END)
        for rest in get_restaurantes():
            listbox.insert(tk.END, f"{rest['nome_rest']} - {rest['endereco']}")

    def adicionar():
        data = {
            "nome_rest": entry_nome.get(),
            "endereco": entry_endereco.get()
        }
        add_restaurante(data)
        refresh_list()

    def atualizar():
        nome = entry_nome.get()
        data = {
            "nome_rest": nome,
            "endereco": entry_endereco.get()
        }
        update_restaurante(nome, data)
        refresh_list()

    def deletar():
        nome = entry_nome.get()
        delete_restaurante(nome)
        refresh_list()

    # Labels e entradas
    tk.Label(window, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(window)
    entry_nome.grid(row=0, column=1)

    tk.Label(window, text="Endereço:").grid(row=1, column=0)
    entry_endereco = tk.Entry(window)
    entry_endereco.grid(row=1, column=1)

    # Botões
    tk.Button(window, text="Adicionar", command=adicionar).grid(row=2, column=0)
    tk.Button(window, text="Atualizar", command=atualizar).grid(row=2, column=1)
    tk.Button(window, text="Deletar", command=deletar).grid(row=2, column=2)

    # Lista
    listbox = tk.Listbox(window, width=80)
    listbox.grid(row=3, column=0, columnspan=3)

    refresh_list()
