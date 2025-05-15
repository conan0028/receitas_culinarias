import tkinter as tk
from tkinter import ttk, messagebox
from api_client_ingredientes_receita import get_ingredientes_receita, add_ingrediente_receita, delete_ingrediente_receita
from api_client_receitas import get_receitas
from api_client_ingredientes import get_ingredientes

def open_ingredientes_receita_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Ingredientes das Receitas")
    window.geometry("900x600")

    def refresh_list():
        try:
            # Limpa a Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Busca todos os relacionamentos
            relacoes = get_ingredientes_receita()
            if isinstance(relacoes, dict) and 'error' in relacoes:
                messagebox.showerror("Erro", relacoes['error'])
                return

            if not relacoes:
                messagebox.showinfo("Informação", "Nenhum ingrediente vinculado a receitas.")
                return

            # Preenche a Treeview
            for rel in relacoes:
                tree.insert('', 'end', values=(
                    rel['cod_rec_ingrec'],
                    rel.get('receita_nome', 'N/A'),
                    rel['cod_ing_ingrec'],
                    rel.get('ingrediente_nome', 'N/A'),
                    rel['quant_ingrec'],
                    rel['med_ingrec']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def carregar_combos():
        try:
            # Carrega receitas
            receitas = get_receitas()
            combo_receita['values'] = [f"{r['cod_rec']} - {r['nome_rec']}" for r in receitas]

            # Carrega ingredientes
            ingredientes = get_ingredientes()
            combo_ingrediente['values'] = [f"{i['cod_ingred']} - {i['nome_ingred']}" for i in ingredientes]
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def adicionar():
        try:
            # Validação
            if not combo_receita.get() or not combo_ingrediente.get() or not entry_quantidade.get() or not combo_medida.get():
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            # Extrai IDs
            cod_rec = int(combo_receita.get().split(" - ")[0])
            cod_ing = int(combo_ingrediente.get().split(" - ")[0])
            quantidade = float(entry_quantidade.get())

            if quantidade <= 0:
                messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
                return

            data = {
                "cod_rec_ingrec": cod_rec,
                "cod_ing_ingrec": cod_ing,
                "quant_ingrec": quantidade,
                "med_ingrec": combo_medida.get()
            }

            # Chama a API
            resultado = add_ingrediente_receita(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Ingrediente vinculado à receita com sucesso!")
                refresh_list()
                limpar_campos()

        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar: {str(e)}")

    def deletar():
        try:
            # Obtém item selecionado
            selected_item = tree.selection()[0]
            item_data = tree.item(selected_item)
            cod_rec = item_data['values'][0]
            cod_ing = item_data['values'][2]

            if messagebox.askyesno("Confirmar", f"Remover este ingrediente da receita?"):
                resultado = delete_ingrediente_receita(cod_rec, cod_ing)
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
        combo_ingrediente.set('')
        entry_quantidade.delete(0, tk.END)
        combo_medida.set('')

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Adicionar Ingrediente à Receita", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    # Combos e campos
    tk.Label(frame_entrada, text="Receita:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo_receita = ttk.Combobox(frame_entrada, width=30)
    combo_receita.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Ingrediente:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    combo_ingrediente = ttk.Combobox(frame_entrada, width=30)
    combo_ingrediente.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_quantidade = tk.Entry(frame_entrada, width=10)
    entry_quantidade.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Medida:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    combo_medida = ttk.Combobox(frame_entrada, width=10, values=["g", "kg", "ml", "L", "xíc.", "colher", "un"])
    combo_medida.grid(row=1, column=3, padx=5, pady=5, sticky="w")

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
    frame_lista = tk.LabelFrame(main_frame, text="Ingredientes Vinculados às Receitas", padx=5, pady=5)
    frame_lista.pack(fill=tk.BOTH, expand=True)

    # Treeview
    columns = ("cod_rec", "receita", "cod_ing", "ingrediente", "quantidade", "medida")
    tree = ttk.Treeview(frame_lista, columns=columns, show="headings", selectmode="browse")

    # Configuração das colunas
    tree.heading("cod_rec", text="Cód. Receita")
    tree.heading("receita", text="Nome Receita")
    tree.heading("cod_ing", text="Cód. Ingrediente")
    tree.heading("ingrediente", text="Nome Ingrediente")
    tree.heading("quantidade", text="Quantidade")
    tree.heading("medida", text="Medida")

    tree.column("cod_rec", width=80, anchor="center")
    tree.column("receita", width=200)
    tree.column("cod_ing", width=80, anchor="center")
    tree.column("ingrediente", width=200)
    tree.column("quantidade", width=80, anchor="center")
    tree.column("medida", width=80, anchor="center")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)

    # Inicialização
    carregar_combos()
    refresh_list()
