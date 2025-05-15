import tkinter as tk
from tkinter import ttk, messagebox
from api_client_inclui import get_inclui, add_inclui, delete_inclui
from api_client_receitas import get_receitas
from api_client_livros import get_livros

def open_inclui_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Relação Receitas-Livros")
    window.geometry("900x600")

    def refresh_list():
        try:
            # Limpa a Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Busca todos os relacionamentos
            relacoes = get_inclui()
            if isinstance(relacoes, dict) and 'error' in relacoes:
                messagebox.showerror("Erro", relacoes['error'])
                return

            if not relacoes:
                messagebox.showinfo("Informação", "Nenhuma receita vinculada a livros.")
                return

            # Preenche a Treeview
            for rel in relacoes:
                tree.insert('', 'end', values=(
                    rel['cod_rec_inc'],
                    rel.get('receita_nome', 'N/A'),
                    rel['titulo_liv_inc'],
                    rel.get('livro_isbn', 'N/A')
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def carregar_combos():
        try:
            # Carrega receitas
            receitas = get_receitas()
            combo_receita['values'] = [f"{r['cod_rec']} - {r['nome_rec']}" for r in receitas]

            # Carrega livros
            livros = get_livros()
            combo_livro['values'] = [f"{l['titulo_livro']} (ISBN: {l['isbn']})" for l in livros]
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def adicionar():
        try:
            # Validação
            if not combo_receita.get() or not combo_livro.get():
                messagebox.showerror("Erro", "Selecione uma receita e um livro!")
                return

            # Extrai dados
            cod_rec = int(combo_receita.get().split(" - ")[0])
            titulo_livro = combo_livro.get().split(" (ISBN:")[0]

            data = {
                "cod_rec_inc": cod_rec,
                "titulo_liv_inc": titulo_livro
            }

            # Chama a API
            resultado = add_inclui(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Receita vinculada ao livro com sucesso!")
                refresh_list()
                limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar: {str(e)}")

    def deletar():
        try:
            # Obtém item selecionado
            selected_item = tree.selection()[0]
            item_data = tree.item(selected_item)
            cod_rec = item_data['values'][0]
            titulo_livro = item_data['values'][2]

            if messagebox.askyesno("Confirmar", f"Remover esta relação?"):
                resultado = delete_inclui(cod_rec, titulo_livro)
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
        combo_receita.set('')
        combo_livro.set('')

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Adicionar Receita a Livro", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    # Combos e campos
    tk.Label(frame_entrada, text="Receita:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo_receita = ttk.Combobox(frame_entrada, width=40)
    combo_receita.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Livro:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    combo_livro = ttk.Combobox(frame_entrada, width=40)
    combo_livro.grid(row=0, column=3, padx=5, pady=5, sticky="w")

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
    frame_lista = tk.LabelFrame(main_frame, text="Receitas Incluídas em Livros", padx=5, pady=5)
    frame_lista.pack(fill=tk.BOTH, expand=True)

    # Treeview
    columns = ("cod_rec", "receita", "livro", "isbn")
    tree = ttk.Treeview(frame_lista, columns=columns, show="headings", selectmode="browse")

    # Configuração das colunas
    tree.heading("cod_rec", text="Cód. Receita")
    tree.heading("receita", text="Nome Receita")
    tree.heading("livro", text="Título do Livro")
    tree.heading("isbn", text="ISBN")

    tree.column("cod_rec", width=100, anchor="center")
    tree.column("receita", width=200)
    tree.column("livro", width=250)
    tree.column("isbn", width=100, anchor="center")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)

    # Inicialização
    carregar_combos()
    refresh_list()
