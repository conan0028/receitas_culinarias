import tkinter as tk
from tkinter import messagebox
from api_client_editores import get_editores, add_editor, update_editor, delete_editor

def open_editores_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Editores")
    window.geometry("800x600")

    def refresh_list():
        try:
            listbox.delete(0, tk.END)
            editores = get_editores()
            if isinstance(editores, dict) and 'error' in editores:
                messagebox.showerror("Erro", editores['error'])
                return

            if not editores:
                messagebox.showinfo("Informação", "Nenhum editor cadastrado.")
            for ed in editores:
                listbox.insert(tk.END, f"{ed['cpf_edit']} - {ed['nome_edit']}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar editores: {str(e)}")

    def validar_campos():
        if not entry_cpf.get():
            messagebox.showerror("Erro", "CPF é obrigatório")
            return False
        if not entry_nome.get():
            messagebox.showerror("Erro", "Nome é obrigatório")
            return False
        if not entry_data.get():
            messagebox.showerror("Erro", "Data de contrato é obrigatória")
            return False
        try:
            salario = float(entry_salario.get())
            if salario < 0:
                messagebox.showerror("Erro", "Salário não pode ser negativo")
                return False
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número válido")
            return False
        return True

    def adicionar():
        if not validar_campos():
            return

        cpf = entry_cpf.get()
        try:
            editores = get_editores()
            if isinstance(editores, dict) and 'error' in editores:
                messagebox.showerror("Erro", editores['error'])
                return

            if any(ed['cpf_edit'] == cpf for ed in editores):
                messagebox.showerror("Erro", f"CPF {cpf} já cadastrado!")
                return

            data = {
                "cpf_edit": cpf,
                "nome_edit": entry_nome.get(),
                "dt_contrato_edit": entry_data.get(),
                "salario_edit": float(entry_salario.get())
            }

            resultado = add_editor(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Editor adicionado com sucesso!")
                refresh_list()
                limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar editor: {str(e)}")

    def atualizar():
        if not validar_campos():
            return

        cpf = entry_cpf.get()
        try:
            editores = get_editores()
            if isinstance(editores, dict) and 'error' in editores:
                messagebox.showerror("Erro", editores['error'])
                return

            if not any(ed['cpf_edit'] == cpf for ed in editores):
                messagebox.showerror("Erro", f"CPF {cpf} não encontrado!")
                return

            data = {
                "nome_edit": entry_nome.get(),
                "dt_contrato_edit": entry_data.get(),
                "salario_edit": float(entry_salario.get())
            }

            resultado = update_editor(cpf, data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Editor atualizado com sucesso!")
                refresh_list()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar editor: {str(e)}")

    def deletar():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um editor para deletar")
            return

        try:
            selected = listbox.get(selection[0])
            cpf = selected.split(" - ")[0]

            if not cpf:
                messagebox.showerror("Erro", "CPF do editor não identificado")
                return

            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o editor {cpf}?"):
                resultado = delete_editor(cpf)

                if isinstance(resultado, dict):
                    if 'error' in resultado:
                        messagebox.showerror("Não é possível excluir", resultado['error'])
                    elif 'message' in resultado:
                        messagebox.showinfo("Sucesso", "Editor deletado com sucesso!")
                        refresh_list()
                        limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar editor: {str(e)}")

    def limpar_campos():
        entry_cpf.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        entry_salario.delete(0, tk.END)

    def on_select(event):
        try:
            selection = listbox.curselection()
            if selection:
                selected = listbox.get(selection[0])
                cpf = selected.split(" - ")[0]
                editores = get_editores()
                if isinstance(editores, dict) and 'error' in editores:
                    messagebox.showerror("Erro", editores['error'])
                    return

                for ed in editores:
                    if ed['cpf_edit'] == cpf:
                        limpar_campos()
                        entry_cpf.insert(0, ed['cpf_edit'])
                        entry_nome.insert(0, ed['nome_edit'])
                        entry_data.insert(0, ed['dt_contrato_edit'])
                        entry_salario.insert(0, str(ed['salario_edit']))
                        break
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Dados do Editor", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    tk.Label(frame_entrada, text="CPF:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    entry_cpf = tk.Entry(frame_entrada, width=20)
    entry_cpf.grid(row=0, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Nome:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    entry_nome = tk.Entry(frame_entrada, width=40)
    entry_nome.grid(row=1, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Data Contrato (AAAA-MM-DD):").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    entry_data = tk.Entry(frame_entrada, width=15)
    entry_data.grid(row=2, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Salário:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
    entry_salario = tk.Entry(frame_entrada, width=15)
    entry_salario.grid(row=3, column=1, sticky="w", pady=2)

    # Frame de botões
    frame_botoes = tk.Frame(main_frame)
    frame_botoes.pack(fill=tk.X, pady=5)

    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar, width=10)
    btn_adicionar.pack(side=tk.LEFT, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar, width=10)
    btn_atualizar.pack(side=tk.LEFT, padx=5)

    btn_deletar = tk.Button(frame_botoes, text="Deletar", command=deletar, width=10)
    btn_deletar.pack(side=tk.LEFT, padx=5)

    btn_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar_campos, width=10)
    btn_limpar.pack(side=tk.LEFT, padx=5)

    # Frame da lista
    frame_lista = tk.LabelFrame(main_frame, text="Lista de Editores", padx=5, pady=5)
    frame_lista.pack(fill=tk.BOTH, expand=True)

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
    listbox.bind('<<ListboxSelect>>', on_select)

    scrollbar.config(command=listbox.yview)

    # Inicializa a lista
    refresh_list()
