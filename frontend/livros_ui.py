import tkinter as tk
from tkinter import messagebox
from api_client_livros import get_livros, add_livro, update_livro, delete_livro

def open_livros_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Livros")

    def refresh_list():
        listbox.delete(0, tk.END)
        for livro in get_livros():
            listbox.insert(tk.END, f"{livro['titulo_livro']} - ISBN: {livro['isbn']}")

    def adicionar():
        data = {
            "titulo_livro": entry_titulo.get(),
            "isbn": int(entry_isbn.get())
        }
        add_livro(data)
        refresh_list()

    def atualizar():
        titulo = entry_titulo.get()
        data = {
            "titulo_livro": titulo,
            "isbn": int(entry_isbn.get())
        }
        update_livro(titulo, data)
        refresh_list()

    def deletar():
        titulo = entry_titulo.get()
        delete_livro(titulo)
        refresh_list()

    # Labels e entradas
    tk.Label(window, text="Título:").grid(row=0, column=0)
    entry_titulo = tk.Entry(window)
    entry_titulo.grid(row=0, column=1)

    tk.Label(window, text="ISBN:").grid(row=1, column=0)
    entry_isbn = tk.Entry(window)
    entry_isbn.grid(row=1, column=1)

    # Botões
    tk.Button(window, text="Adicionar", command=adicionar).grid(row=2, column=0)
    tk.Button(window, text="Atualizar", command=atualizar).grid(row=2, column=1)
    tk.Button(window, text="Deletar", command=deletar).grid(row=2, column=2)

    # Lista
    listbox = tk.Listbox(window, width=80)
    listbox.grid(row=3, column=0, columnspan=3)

    refresh_list()
