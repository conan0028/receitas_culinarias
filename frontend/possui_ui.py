import tkinter as tk
from tkinter import messagebox
from api_client_possui import create_possui, delete_possui
from frontend.api_client_receitas import get_receitas
from api_client_editores import get_editores

def open_possui_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Relações Editor-Receita")
    window.geometry("800x600")

    def refresh_list():
        try:
            listbox.delete(0, tk.END)
            # Carrega todas as relações existentes
            editores = get_editores()
            for editor in editores:
                if 'possui' in editor and editor['possui']:
                    for receita in editor['possui']:
                        listbox.insert(
                            tk.END,
                            f"Editor: {editor['cpf_edit']} - {editor['nome_edit']} | "
                            f"Receita: {receita['cod_rec']} - {receita.get('nome_rec', 'N/A')}"
                        )
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar relações: {str(e)}")

    def validar_campos():
        if not combo_editor.get():
            messagebox.showerror("Erro", "Selecione um editor")
            return False
        if not combo_receita.get():
            messagebox.showerror("Erro", "Selecione uma receita")
            return False
        return True

    def carregar_combos():
        try:
            # Carrega editores
            editores = get_editores()
            combo_editor['values'] = [f"{e['cpf_edit']} - {e['nome_edit']}" for e in editores]

            # Carrega receitas
            receitas = get_receitas()
            combo_receita['values'] = [f"{r['cod_rec']} - {r['nome_rec']}" for r in receitas]
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def adicionar():
        if not validar_campos():
            return

        try:
            cpf_edit = combo_editor.get().split(" - ")[0]
            cod_rec = combo_receita.get().split(" - ")[0]

            data = {
                "cpf_edit_pos": cpf_edit,
                "cod_rec_pos": int(cod_rec)
            }

            resultado = create_possui(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Relação criada com sucesso!")
                refresh_list()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar relação: {str(e)}")

    def deletar():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma relação para deletar")
            return

        try:
            selected = listbox.get(selection[0])
            parts = selected.split(" | ")
            cpf_edit = parts[0].split(" - ")[1].strip()
            cod_rec = parts[1].split(" - ")[1].strip()

            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar esta relação?"):
                resultado = delete_possui(int(cod_rec), cpf_edit)
                if isinstance(resultado, dict) and 'error' in resultado:
                    messagebox.showerror("Erro", resultado['error'])
                else:
                    messagebox.showinfo("Sucesso", "Relação deletada com sucesso!")
                    refresh_list()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar relação: {str(e)}")

    def limpar_campos():
        combo_editor.set('')
        combo_receita.set('')

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Nova Relação Editor-Receita", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    # Combos para seleção
    tk.Label(frame_entrada, text="Editor:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    combo_editor = tk.ttk.Combobox(frame_entrada, width=40)
    combo_editor.grid(row=0, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Receita:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    combo_receita = tk.ttk.Combobox(frame_entrada, width=40)
    combo_receita.grid(row=1, column=1, sticky="w", pady=2)

    # Frame de botões
    frame_botoes = tk.Frame(main_frame)
    frame_botoes.pack(fill=tk.X, pady=5)

    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar, width=10)
    btn_adicionar.pack(side=tk.LEFT, padx=5)

    btn_deletar = tk.Button(frame_botoes, text="Deletar", command=deletar, width=10)
    btn_deletar.pack(side=tk.LEFT, padx=5)

    btn_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar_campos, width=10)
    btn_limpar.pack(side=tk.LEFT, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=refresh_list, width=10)
    btn_atualizar.pack(side=tk.LEFT, padx=5)

    # Frame da lista
    frame_lista = tk.LabelFrame(main_frame, text="Relações Existentes", padx=5, pady=5)
    frame_lista.pack(fill=tk.BOTH, expand=True)

    # Lista com scrollbar
    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(
        frame_lista,
        width=80,
        height=15,
        yscrollcommand=scrollbar.set,
        selectmode=tk.SINGLE
    )
    listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=listbox.yview)

    # Inicializa os combos e a lista
    carregar_combos()
    refresh_list()
