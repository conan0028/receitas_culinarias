# import tkinter as tk
# root = tk.Tk()
# root.title("Teste Tkinter")
# tk.Label(root, text="Funcionou!").pack()
# root.mainloop()

import tkinter as tk

def mostrar_tamanho():
    largura = janela.winfo_width()   # Largura atual da janela
    altura = janela.winfo_height()   # Altura atual da janela
    print(f"Largura: {largura}px, Altura: {altura}px")

janela = tk.Tk()
janela.title("Descobrir Tamanho")
janela.geometry("400x300")  # Define um tamanho inicial (opcional)

# Botão para mostrar o tamanho atual
btn = tk.Button(janela, text="Mostrar Tamanho", command=mostrar_tamanho)
btn.pack(pady=20)

janela.mainloop()