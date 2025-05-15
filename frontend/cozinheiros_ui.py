import tkinter as tk
from tkinter import messagebox
from api_client_cozinheiros import get_cozinheiros, add_cozinheiro, update_cozinheiro, delete_cozinheiro

def open_cozinheiros_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Cozinheiros")
    window.geometry("800x600")

    def refresh_list():
        try:
            listbox.delete(0, tk.END)
            cozinheiros = get_cozinheiros()
            if not cozinheiros:
                messagebox.showinfo("Informação", "Nenhum cozinheiro cadastrado.")
            for coz in cozinheiros:
                listbox.insert(tk.END, f"{coz['cpf_coz']} - {coz['nome_coz']} ({coz['nome_fantasia']})")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar cozinheiros: {str(e)}")

    def validar_campos():
        if not entry_cpf.get():
            messagebox.showerror("Erro", "CPF é obrigatório")
            return False
        if not entry_nome.get():
            messagebox.showerror("Erro", "Nome é obrigatório")
            return False
        if not entry_fantasia.get():
            messagebox.showerror("Erro", "Nome fantasia é obrigatório")
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
            cozinheiros = get_cozinheiros()
            if any(coz['cpf_coz'] == cpf for coz in cozinheiros):
                messagebox.showerror("Erro", f"CPF {cpf} já cadastrado!")
                return

            data = {
                "cpf_coz": cpf,
                "nome_coz": entry_nome.get(),
                "nome_fantasia": entry_fantasia.get(),
                "dt_contrato_coz": entry_data.get(),
                "salario_coz": float(entry_salario.get())
            }

            resultado = add_cozinheiro(data)
            if resultado:
                messagebox.showinfo("Sucesso", "Cozinheiro adicionado com sucesso!")
                refresh_list()
                limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar cozinheiro: {str(e)}")

    def atualizar():
        if not validar_campos():
            return

        cpf = entry_cpf.get()
        try:
            cozinheiros = get_cozinheiros()
            if not any(coz['cpf_coz'] == cpf for coz in cozinheiros):
                messagebox.showerror("Erro", f"CPF {cpf} não encontrado!")
                return

            data = {
                "nome_coz": entry_nome.get(),
                "nome_fantasia": entry_fantasia.get(),
                "dt_contrato_coz": entry_data.get(),
                "salario_coz": float(entry_salario.get())
            }

            resultado = update_cozinheiro(cpf, data)
            if resultado:
                messagebox.showinfo("Sucesso", "Cozinheiro atualizado com sucesso!")
                refresh_list()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar cozinheiro: {str(e)}")

    def deletar():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione um cozinheiro para deletar")
            return

        try:
            selected = listbox.get(selection[0])
            cpf = selected.split(" - ")[0]

            if not cpf:
                messagebox.showerror("Erro", "CPF do cozinheiro não identificado")
                return

            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar o cozinheiro {cpf}?"):
                resultado = delete_cozinheiro(cpf)

                if isinstance(resultado, dict) and 'error' in resultado:
                    messagebox.showerror("Não é possível excluir", resultado['error'])
                else:
                    messagebox.showinfo("Sucesso", "Cozinheiro deletado com sucesso!")
                    refresh_list()
                    limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar cozinheiro: {str(e)}")

    def limpar_campos():
        entry_cpf.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_fantasia.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        entry_salario.delete(0, tk.END)

    def on_select(event):
        try:
            selection = listbox.curselection()
            if selection:
                selected = listbox.get(selection[0])
                cpf = selected.split(" - ")[0]
                for coz in get_cozinheiros():
                    if coz['cpf_coz'] == cpf:
                        limpar_campos()
                        entry_cpf.insert(0, coz['cpf_coz'])
                        entry_nome.insert(0, coz['nome_coz'])
                        entry_fantasia.insert(0, coz['nome_fantasia'])
                        entry_data.insert(0, coz['dt_contrato_coz'])
                        entry_salario.insert(0, str(coz['salario_coz']))
                        break
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Dados do Cozinheiro", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    tk.Label(frame_entrada, text="CPF:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    entry_cpf = tk.Entry(frame_entrada, width=20)
    entry_cpf.grid(row=0, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Nome:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    entry_nome = tk.Entry(frame_entrada, width=40)
    entry_nome.grid(row=1, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Nome Fantasia:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    entry_fantasia = tk.Entry(frame_entrada, width=40)
    entry_fantasia.grid(row=2, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Data Contrato (AAAA-MM-DD):").grid(row=3, column=0, sticky="e", padx=5, pady=2)
    entry_data = tk.Entry(frame_entrada, width=15)
    entry_data.grid(row=3, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Salário:").grid(row=4, column=0, sticky="e", padx=5, pady=2)
    entry_salario = tk.Entry(frame_entrada, width=15)
    entry_salario.grid(row=4, column=1, sticky="w", pady=2)

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
    frame_lista = tk.LabelFrame(main_frame, text="Lista de Cozinheiros", padx=5, pady=5)
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
