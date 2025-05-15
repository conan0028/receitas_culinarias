import tkinter as tk
from cozinheiros_ui import open_cozinheiros_ui

root = tk.Tk()
root.title("Receitas Culinárias")

tk.Button(root, text="Gerenciar Cozinheiros", command=lambda: open_cozinheiros_ui(root)).pack(pady=20)

# Aqui no futuro: adicionar mais botões para novas tabelas
# ex: tk.Button(root, text="Gerenciar Ingredientes", command=lambda: open_ingredientes_ui(root)).pack()

root.mainloop()
