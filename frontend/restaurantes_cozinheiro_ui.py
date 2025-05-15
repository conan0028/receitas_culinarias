import tkinter as tk
from tkinter import ttk, messagebox
from api_client_restaurantes_cozinheiro import get_restaurantes_cozinheiro, add_restaurante_cozinheiro, delete_restaurante_cozinheiro
from api_client_cozinheiros import get_cozinheiros
from api_client_restaurantes import get_restaurantes

def open_restaurantes_cozinheiro_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Relação Cozinheiros-Restaurantes")
    window.geometry("1000x600")

    def refresh_list():
        try:
            # Limpa a Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Busca todos os relacionamentos
            relacoes = get_restaurantes_cozinheiro()
            if isinstance(relacoes, dict) and 'error' in relacoes:
                messagebox.showerror("Erro", relacoes['error'])
                return

            if not relacoes:
                messagebox.showinfo("Informação", "Nenhum cozinheiro vinculado a restaurantes.")
                return

            # Preenche a Treeview
            for rel in relacoes:
                tree.insert('', 'end', values=(
                    rel['cod_coz_restcoz'],
                    rel.get('cozinheiro_nome', 'N/A'),
                    rel['nome_rest_restcoz'],
                    rel.get('restaurante_endereco', 'N/A'),
                    rel['dt_contratacao']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def carregar_combos():
        try:
            # Carrega cozinheiros
            cozinheiros = get_cozinheiros()
            combo_cozinheiro['values'] = [f"{c['cpf_coz']} - {c['nome_coz']}" for c in cozinheiros]

            # Carrega restaurantes
            restaurantes = get_restaurantes()
            combo_restaurante['values'] = [f"{r['nome_rest']} - {r['endereco']}" for r in restaurantes]

            # Atualiza data para hoje
            import datetime
            entry_data.delete(0, tk.END)
            entry_data.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def adicionar():
        try:
            # Validação
            if not combo_cozinheiro.get() or not combo_restaurante.get() or not entry_data.get():
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            # Extrai dados
            cpf_coz = combo_cozinheiro.get().split(" - ")[0]
            nome_rest = combo_restaurante.get().split(" - ")[0]
            data_contratacao = entry_data.get()

            data = {
                "cod_coz_restcoz": cpf_coz,
                "nome_rest_restcoz": nome_rest,
                "dt_contratacao": data_contratacao
            }

            # Chama a API
            resultado = add_restaurante_cozinheiro(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Cozinheiro vinculado ao restaurante com sucesso!")
                refresh_list()
                limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar: {str(e)}")

    def deletar():
        try:
            # Obtém item selecionado
            selected_item = tree.selection()[0]
            item_data = tree.item(selected_item)
            cpf_coz = item_data['values'][0]
            nome_rest = item_data['values'][2]

            if messagebox.askyesno("Confirmar", f"Remover esta relação?"):
                resultado = delete_restaurante_cozinheiro(cpf_coz, nome_rest)
                if isinstance(resultado, dict) and 'error' in resultado:
                    messagebox.showerror("Erro", resultado['error'])
                else:
                    messagebox.showinfo("Sucesso", "Relação removida com sucesso!")
                    refresh_list()

        except IndexError:
            messagebox.showerror("Erro", "Selecione um item para remover!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao remover: {str(e)}")

    def limpar_campos():
        combo_cozinheiro.set('')
        combo_restaurante.set('')
        import datetime
        entry_data.delete(0, tk.END)
        entry_data.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Vincular Cozinheiro a Restaurante", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    # Combos e campos
    tk.Label(frame_entrada, text="Cozinheiro:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo_cozinheiro = ttk.Combobox(frame_entrada, width=40)
    combo_cozinheiro.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Restaurante:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    combo_restaurante = ttk.Combobox(frame_entrada, width=40)
    combo_restaurante.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Data Contratação:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_data = tk.Entry(frame_entrada, width=15)
    entry_data.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Frame de botões
    frame_botoes = tk.Frame(main_frame)
    frame_botoes.pack(fill=tk.X, pady=5)

    btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar, width=15)
    btn_adicionar.pack(side=tk.LEFT, padx=5)

    btn_deletar = tk.Button(frame_botoes, text="Remover Selecionado", command=deletar, width=15)
    btn_deletar.pack(side=tk.LEFT, padx=5)

    btn_limpar = tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos, width=15)
    btn_limpar.pack(side=tk.LEFT, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="Atualizar Lista", command=refresh_list, width=15)
    btn_atualizar.pack(side=tk.LEFT, padx=5)

    # Frame da lista
    frame_lista = tk.LabelFrame(main_frame, text="Cozinheiros Vinculados a Restaurantes", padx=5, pady=5)
    frame_lista.pack(fill=tk.BOTH, expand=True)

    # Treeview
    columns = ("cpf_cozinheiro", "nome_cozinheiro", "restaurante", "endereco", "data_contratacao")
    tree = ttk.Treeview(frame_lista, columns=columns, show="headings", selectmode="browse")

    # Configuração das colunas
    tree.heading("cpf_cozinheiro", text="CPF Cozinheiro")
    tree.heading("nome_cozinheiro", text="Nome Cozinheiro")
    tree.heading("restaurante", text="Restaurante")
    tree.heading("endereco", text="Endereço")
    tree.heading("data_contratacao", text="Data Contratação")

    tree.column("cpf_cozinheiro", width=120, anchor="center")
    tree.column("nome_cozinheiro", width=200)
    tree.column("restaurante", width=200)
    tree.column("endereco", width=250)
    tree.column("data_contratacao", width=120, anchor="center")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)

    # Inicialização
    carregar_combos()
    refresh_list()
