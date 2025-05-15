import tkinter as tk
from tkinter import messagebox
from api_client_empregados_rg import get_empregados_rg, add_empregado_rg, update_empregado_rg, delete_empregado_rg

def open_empregados_rg_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Empregados RG")

    def refresh_list():
        listbox.delete(0, tk.END)
        for emp in get_empregados_rg():
            listbox.insert(tk.END, f"{emp['rg']} - Salário: {emp['salario']}")

    def adicionar():
        data = {
            "rg": entry_rg.get(),
            "salario": float(entry_salario.get())
        }
        add_empregado_rg(data)
        refresh_list()

    def atualizar():
        rg = entry_rg.get()
        data = {
            "rg": rg,
            "salario": float(entry_salario.get())
        }
        update_empregado_rg(rg, data)
        refresh_list()

    def deletar():
        rg = entry_rg.get()
        delete_empregado_rg(rg)
        refresh_list()

    # Labels e entradas
    tk.Label(window, text="RG:").grid(row=0, column=0)
    entry_rg = tk.Entry(window)
    entry_rg.grid(row=0, column=1)

    tk.Label(window, text="Salário:").grid(row=1, column=0)
    entry_salario = tk.Entry(window)
    entry_salario.grid(row=1, column=1)

    # Botões
    tk.Button(window, text="Adicionar", command=adicionar).grid(row=2, column=0)
    tk.Button(window, text="Atualizar", command=atualizar).grid(row=2, column=1)
    tk.Button(window, text="Deletar", command=deletar).grid(row=2, column=2)

    # Lista
    listbox = tk.Listbox(window, width=80)
    listbox.grid(row=3, column=0, columnspan=3)

    refresh_list()
