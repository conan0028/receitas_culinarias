import tkinter as tk
from tkinter import ttk, messagebox
from api_client_testa import get_testa, add_testa, delete_testa
from api_client_degustadores import get_degustadores
from api_client_receitas import get_receitas
from datetime import datetime

def open_testa_ui(master):
    window = tk.Toplevel(master)
    window.title("Avaliação de Receitas por Degustadores")
    window.geometry("1000x600")

    def refresh_list():
        try:
            # Limpa a Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Busca todas as avaliações
            avaliacoes = get_testa()
            if isinstance(avaliacoes, dict) and 'error' in avaliacoes:
                messagebox.showerror("Erro", avaliacoes['error'])
                return

            if not avaliacoes:
                messagebox.showinfo("Informação", "Nenhuma avaliação registrada.")
                return

            # Preenche a Treeview
            for aval in avaliacoes:
                tree.insert('', 'end', values=(
                    aval['cod_rec_test'],
                    aval.get('receita_nome', 'N/A'),
                    aval['cpf_deg_test'],
                    aval.get('degustador_nome', 'N/A'),
                    aval['dt_test'],
                    aval['nota_test']
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar avaliações: {str(e)}")

    def carregar_combos():
        try:
            # Carrega degustadores
            degustadores = get_degustadores()
            combo_degustador['values'] = [f"{d['cpf_deg']} - {d['nome_deg']}" for d in degustadores]

            # Carrega receitas
            receitas = get_receitas()
            combo_receita['values'] = [f"{r['cod_rec']} - {r['nome_rec']}" for r in receitas]

            # Atualiza data para hoje
            entry_data.delete(0, tk.END)
            entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))

            # Limpa nota
            entry_nota.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def adicionar():
        try:
            # Validação
            if not combo_degustador.get() or not combo_receita.get() or not entry_data.get() or not entry_nota.get():
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return

            # Extrai dados
            cpf_deg = combo_degustador.get().split(" - ")[0]
            cod_rec = int(combo_receita.get().split(" - ")[0])
            data_teste = entry_data.get()
            nota = int(entry_nota.get())

            if nota < 0 or nota > 10:
                messagebox.showerror("Erro", "Nota deve ser entre 0 e 10!")
                return

            data = {
                "cod_rec_test": cod_rec,
                "cpf_deg_test": cpf_deg,
                "dt_test": data_teste,
                "nota_test": nota
            }

            # Chama a API
            resultado = add_testa(data)
            if isinstance(resultado, dict) and 'error' in resultado:
                messagebox.showerror("Erro", resultado['error'])
            else:
                messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso!")
                refresh_list()
                limpar_campos()

        except ValueError:
            messagebox.showerror("Erro", "Nota deve ser um número inteiro!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar avaliação: {str(e)}")

    def deletar():
        try:
            # Obtém item selecionado
            selected_item = tree.selection()[0]
            item_data = tree.item(selected_item)
            cod_rec = item_data['values'][0]
            cpf_deg = item_data['values'][2]

            if messagebox.askyesno("Confirmar", f"Remover esta avaliação?"):
                resultado = delete_testa(cod_rec, cpf_deg)
                if isinstance(resultado, dict) and 'error' in resultado:
                    messagebox.showerror("Erro", resultado['error'])
                else:
                    messagebox.showinfo("Sucesso", "Avaliação removida com sucesso!")
                    refresh_list()

        except IndexError:
            messagebox.showerror("Erro", "Selecione uma avaliação para remover!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao remover avaliação: {str(e)}")

    def limpar_campos():
        combo_degustador.set('')
        combo_receita.set('')
        entry_data.delete(0, tk.END)
        entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        entry_nota.delete(0, tk.END)

    # Frame principal
    main_frame = tk.Frame(window, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Frame de entrada de dados
    frame_entrada = tk.LabelFrame(main_frame, text="Nova Avaliação", padx=5, pady=5)
    frame_entrada.pack(fill=tk.X, pady=5)

    # Combos e campos
    tk.Label(frame_entrada, text="Degustador:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    combo_degustador = ttk.Combobox(frame_entrada, width=30)
    combo_degustador.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Receita:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    combo_receita = ttk.Combobox(frame_entrada, width=30)
    combo_receita.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Data:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_data = tk.Entry(frame_entrada, width=15)
    entry_data.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_entrada, text="Nota (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    entry_nota = tk.Entry(frame_entrada, width=5)
    entry_nota.grid(row=1, column=3, padx=5, pady=5, sticky="w")

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
    frame_lista = tk.LabelFrame(main_frame, text="Avaliações Registradas", padx=5, pady=5)
    frame_lista.pack(fill=tk.BOTH, expand=True)

    # Treeview
    columns = ("cod_rec", "receita", "cpf_deg", "degustador", "data", "nota")
    tree = ttk.Treeview(frame_lista, columns=columns, show="headings", selectmode="browse")

    # Configuração das colunas
    tree.heading("cod_rec", text="Cód. Receita")
    tree.heading("receita", text="Nome Receita")
    tree.heading("cpf_deg", text="CPF Degustador")
    tree.heading("degustador", text="Nome Degustador")
    tree.heading("data", text="Data Avaliação")
    tree.heading("nota", text="Nota (0-10)")

    tree.column("cod_rec", width=80, anchor="center")
    tree.column("receita", width=200)
    tree.column("cpf_deg", width=120, anchor="center")
    tree.column("degustador", width=200)
    tree.column("data", width=100, anchor="center")
    tree.column("nota", width=80, anchor="center")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)

    # Inicialização
    carregar_combos()
    refresh_list()
