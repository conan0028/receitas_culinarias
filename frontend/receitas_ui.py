import tkinter as tk
from tkinter import ttk, messagebox
from api_client_receitas import get_receitas, add_receita, update_receita, delete_receita
from api_client_cozinheiros import get_cozinheiros
from api_client_categorias import get_categorias
from api_client_livros import get_livros
from api_client_ingredientes import get_ingredientes
from api_client_ingredientes_receita import add_ingrediente_receita, delete_ingrediente_receita

def open_receitas_ui(master):
    window = tk.Toplevel(master)
    window.title("Gerenciar Receitas")
    window.geometry("1000x700")

    # Variáveis para ingredientes
    ingredientes_receita = []

    def refresh_list():
        try:
            listbox.delete(0, tk.END)
            receitas = get_receitas()
            if isinstance(receitas, dict) and 'error' in receitas:
                messagebox.showerror("Erro", receitas['error'])
                return

            if not receitas:
                messagebox.showinfo("Informação", "Nenhuma receita cadastrada.")
            for rec in receitas:
                listbox.insert(tk.END, f"{rec['cod_rec']} - {rec['nome_rec']}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar receitas: {str(e)}")

    def carregar_combos():
        try:
            # Carrega cozinheiros
            cozinheiros = get_cozinheiros()
            combo_cozinheiro['values'] = [f"{c['cpf_coz']} - {c['nome_coz']}" for c in cozinheiros]

            # Carrega categorias
            categorias = get_categorias()
            combo_categoria['values'] = [f"{cat['cod_categoria']} - {cat['desc_categoria']}" for cat in categorias]

            # Carrega livros
            livros = get_livros()
            combo_livro['values'] = [f"{livro['isbn']} - {livro['titulo_livro']}" for livro in livros]

            # Carrega ingredientes
            ingredientes = get_ingredientes()
            combo_ingrediente['values'] = [f"{ing['cod_ingred']} - {ing['nome_ingred']}" for ing in ingredientes]

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def validar_campos():
        if not entry_codigo.get():
            messagebox.showerror("Erro", "Código é obrigatório")
            return False
        if not entry_nome.get():
            messagebox.showerror("Erro", "Nome é obrigatório")
            return False
        if not entry_data.get():
            messagebox.showerror("Erro", "Data de criação é obrigatória")
            return False
        if not combo_cozinheiro.get():
            messagebox.showerror("Erro", "Cozinheiro é obrigatório")
            return False
        if not combo_categoria.get():
            messagebox.showerror("Erro", "Categoria é obrigatória")
            return False
        if not combo_livro.get():
            messagebox.showerror("Erro", "Livro é obrigatório")
            return False
        return True

    def adicionar_ingrediente():
        try:
            ingrediente = combo_ingrediente.get()
            quantidade = entry_quantidade.get()
            medida = combo_medida.get()

            if not ingrediente or not quantidade or not medida:
                messagebox.showerror("Erro", "Preencha todos os campos do ingrediente")
                return

            cod_ingred = ingrediente.split(" - ")[0]
            ingredientes_receita.append({
                'cod_ing_ingrec': int(cod_ingred),
                'quant_ingrec': float(quantidade),
                'med_ingrec': medida
            })

            tree_ingredientes.insert('', 'end', values=(
                ingrediente.split(" - ")[1],
                quantidade,
                medida
            ))

            combo_ingrediente.set('')
            entry_quantidade.delete(0, tk.END)
            combo_medida.set('')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar ingrediente: {str(e)}")

    def remover_ingrediente():
        try:
            selected_item = tree_ingredientes.selection()[0]
            index = int(tree_ingredientes.index(selected_item))
            ingredientes_receita.pop(index)
            tree_ingredientes.delete(selected_item)
        except IndexError:
            messagebox.showerror("Erro", "Selecione um ingrediente para remover")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover ingrediente: {str(e)}")

    def adicionar():
        if not validar_campos():
            return

        try:
            data = {
                "cod_rec": int(entry_codigo.get()),
                "nome_rec": entry_nome.get(),
                "dt_criacao_rec": entry_data.get(),
                "cod_categoria_rec": int(combo_categoria.get().split(" - ")[0]),
                "cpf_coz": combo_cozinheiro.get().split(" - ")[0],
                "isbn_rec": int(combo_livro.get().split(" - ")[0]),
                "ingredientes": ingredientes_receita
            }

            resultado = add_receita(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Receita adicionada com sucesso!")
                refresh_list()
                limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar receita: {str(e)}")

    def atualizar():
        if not validar_campos():
            return

        try:
            data = {
                "cod_rec": int(entry_codigo.get()),
                "nome_rec": entry_nome.get(),
                "dt_criacao_rec": entry_data.get(),
                "cod_categoria_rec": int(combo_categoria.get().split(" - ")[0]),
                "cpf_coz": combo_cozinheiro.get().split(" - ")[0],
                "isbn_rec": int(combo_livro.get().split(" - ")[0]),
                "ingredientes": ingredientes_receita
            }

            resultado = update_receita(data['cod_rec'], data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Receita atualizada com sucesso!")
                refresh_list()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar receita: {str(e)}")

    def deletar():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma receita para deletar")
            return

        try:
            selected = listbox.get(selection[0])
            cod_rec = int(selected.split(" - ")[0])

            if messagebox.askyesno("Confirmar", f"Tem certeza que deseja deletar a receita {cod_rec}?"):
                resultado = delete_receita(cod_rec)
                if isinstance(resultado, dict) and 'error' in resultado:
                    messagebox.showerror("Erro", resultado['error'])
                else:
                    messagebox.showinfo("Sucesso", "Receita deletada com sucesso!")
                    refresh_list()
                    limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao deletar receita: {str(e)}")

    def limpar_campos():
        entry_codigo.delete(0, tk.END)
        entry_nome.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        combo_cozinheiro.set('')
        combo_categoria.set('')
        combo_livro.set('')
        ingredientes_receita.clear()
        tree_ingredientes.delete(*tree_ingredientes.get_children())

    def on_select(event):
        try:
            selection = listbox.curselection()
            if selection:
                selected = listbox.get(selection[0])
                cod_rec = int(selected.split(" - ")[0])

                receitas = get_receitas()
                if isinstance(receitas, dict) and 'error' in receitas:
                    messagebox.showerror("Erro", receitas['error'])
                    return

                for rec in receitas:
                    if rec['cod_rec'] == cod_rec:
                        limpar_campos()
                        entry_codigo.insert(0, str(rec['cod_rec']))
                        entry_nome.insert(0, rec['nome_rec'])
                        entry_data.insert(0, rec['dt_criacao_rec'])

                        # Seleciona cozinheiro
                        cozinheiro_str = f"{rec['cpf_coz']} - {rec.get('cozinheiro_nome', '')}"
                        combo_cozinheiro.set(cozinheiro_str)

                        # Seleciona categoria
                        categoria_str = f"{rec['cod_categoria_rec']} - {rec.get('categoria_desc', '')}"
                        combo_categoria.set(categoria_str)

                        # Seleciona livro
                        livro_str = f"{rec['isbn_rec']} - {rec.get('livro_titulo', '')}"
                        combo_livro.set(livro_str)

                        # Carrega ingredientes
                        ingredientes_receita.clear()
                        tree_ingredientes.delete(*tree_ingredientes.get_children())
                        if 'ingredientes' in rec:
                            for ing in rec['ingredientes']:
                                ingredientes_receita.append({
                                    'cod_ing_ingrec': ing['cod_ingred'],
                                    'quant_ingrec': ing['quant_ingrec'],
                                    'med_ingrec': ing['med_ingrec']
                                })
                                tree_ingredientes.insert('', 'end', values=(
                                    ing.get('ingrediente_nome', ''),
                                    ing['quant_ingrec'],
                                    ing['med_ingrec']
                                ))
                        break
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Dados da Receita", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    # Campos básicos
    tk.Label(frame_entrada, text="Código:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    entry_codigo = tk.Entry(frame_entrada, width=10)
    entry_codigo.grid(row=0, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Nome:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
    entry_nome = tk.Entry(frame_entrada, width=30)
    entry_nome.grid(row=0, column=3, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Data Criação (AAAA-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    entry_data = tk.Entry(frame_entrada, width=15)
    entry_data.grid(row=1, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Cozinheiro:").grid(row=1, column=2, sticky="e", padx=5, pady=2)
    combo_cozinheiro = ttk.Combobox(frame_entrada, width=30)
    combo_cozinheiro.grid(row=1, column=3, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Categoria:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    combo_categoria = ttk.Combobox(frame_entrada, width=30)
    combo_categoria.grid(row=2, column=1, sticky="w", pady=2)

    tk.Label(frame_entrada, text="Livro:").grid(row=2, column=2, sticky="e", padx=5, pady=2)
    combo_livro = ttk.Combobox(frame_entrada, width=30)
    combo_livro.grid(row=2, column=3, sticky="w", pady=2)

    # Frame de ingredientes
    frame_ingredientes = tk.LabelFrame(main_frame, text="Ingredientes", padx=5, pady=5)
    frame_ingredientes.pack(fill=tk.X, pady=5)

    # Controles de ingredientes
    tk.Label(frame_ingredientes, text="Ingrediente:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    combo_ingrediente = ttk.Combobox(frame_ingredientes, width=25)
    combo_ingrediente.grid(row=0, column=1, sticky="w", pady=2)

    tk.Label(frame_ingredientes, text="Quantidade:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
    entry_quantidade = tk.Entry(frame_ingredientes, width=10)
    entry_quantidade.grid(row=0, column=3, sticky="w", pady=2)

    tk.Label(frame_ingredientes, text="Medida:").grid(row=0, column=4, sticky="e", padx=5, pady=2)
    combo_medida = ttk.Combobox(frame_ingredientes, width=10, values=["g", "kg", "ml", "L", "xíc.", "colher", "un"])
    combo_medida.grid(row=0, column=5, sticky="w", pady=2)

    btn_add_ingrediente = tk.Button(frame_ingredientes, text="Adicionar", command=adicionar_ingrediente)
    btn_add_ingrediente.grid(row=0, column=6, padx=5)

    btn_rem_ingrediente = tk.Button(frame_ingredientes, text="Remover", command=remover_ingrediente)
    btn_rem_ingrediente.grid(row=0, column=7, padx=5)

    # Treeview para ingredientes
    columns = ('ingrediente', 'quantidade', 'medida')
    tree_ingredientes = ttk.Treeview(frame_ingredientes, columns=columns, show='headings', height=5)
    tree_ingredientes.heading('ingrediente', text='Ingrediente')
    tree_ingredientes.heading('quantidade', text='Quantidade')
    tree_ingredientes.heading('medida', text='Medida')
    tree_ingredientes.column('ingrediente', width=200)
    tree_ingredientes.column('quantidade', width=100)
    tree_ingredientes.column('medida', width=100)
    tree_ingredientes.grid(row=1, column=0, columnspan=8, sticky="nsew", pady=5)

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

    btn_atualizar_lista = tk.Button(frame_botoes, text="Atualizar Lista", command=refresh_list, width=12)
    btn_atualizar_lista.pack(side=tk.LEFT, padx=5)

    # Frame da lista
    frame_lista = tk.LabelFrame(main_frame, text="Lista de Receitas", padx=5, pady=5)
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
    listbox.bind('<<ListboxSelect>>', on_select)

    scrollbar.config(command=listbox.yview)

    # Configuração de expansão
    frame_ingredientes.grid_rowconfigure(1, weight=1)
    frame_ingredientes.grid_columnconfigure(0, weight=1)

    # Inicialização
    carregar_combos()
    refresh_list()
