import tkinter as tk
from cozinheiros_ui import open_cozinheiros_ui
from degustadores_ui import open_degustadores_ui
from editores_ui import open_editores_ui
from livros_ui import open_livros_ui
from restaurantes_ui import open_restaurantes_ui
from categorias_ui import open_categorias_ui
from ingredientes_ui import open_ingredientes_ui
from empregados_rg_ui import open_empregados_rg_ui
from receitas_ui import open_receitas_ui
from inclui_ui import open_inclui_ui
from ingredientes_receita_ui import open_ingredientes_receita_ui
from restaurantes_cozinheiro_ui import open_restaurantes_cozinheiro_ui
from testa_ui import open_testa_ui
from possui_ui import open_possui_ui

# Paleta de cores
BG_COLOR = "#f0f4f8"
BTN_COLOR = "#4f6d7a"
BTN_HOVER = "#688e99"
BTN_TEXT_COLOR = "#ffffff"
BTN_REL_COLOR = "#3a5a6b"  # Cor diferente para tabelas de relacionamento

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Receitas Culinárias - Sistema Completo")
        # Largura: 622px, Altura: 631px
        self.geometry("622x631")
        self.configure(bg=BG_COLOR)

        # Frame principal com scrollbar
        self.main_frame = tk.Frame(self, bg=BG_COLOR)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas e scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg=BG_COLOR)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Criar os botões
        self.create_buttons()

    def on_enter(self, e):
        e.widget["background"] = BTN_HOVER

    def on_leave(self, e):
        if "Tabela:" in e.widget["text"]:
            e.widget["background"] = BTN_REL_COLOR
        else:
            e.widget["background"] = BTN_COLOR

    def create_buttons(self):
        # Tabelas principais
        main_tables = [
            ("Cozinheiros", lambda: open_cozinheiros_ui(self)),
            ("Degustadores", lambda: open_degustadores_ui(self)),
            ("Editores", lambda: open_editores_ui(self)),
            ("Livros", lambda: open_livros_ui(self)),
            ("Restaurantes", lambda: open_restaurantes_ui(self)),
            ("Categorias", lambda: open_categorias_ui(self)),
            ("Ingredientes", lambda: open_ingredientes_ui(self)),
            ("Empregados RG", lambda: open_empregados_rg_ui(self)),
            ("Receitas", lambda: open_receitas_ui(self))
        ]

        # Tabelas de relacionamento
        rel_tables = [
            ("Tabela: Inclui (Livros-Receitas)", lambda: open_inclui_ui(self)),
            ("Tabela: Ingredientes-Receita", lambda: open_ingredientes_receita_ui(self)),
            ("Tabela: Restaurantes-Cozinheiro", lambda: open_restaurantes_cozinheiro_ui(self)),
            ("Tabela: Testa (Degustadores-Receitas)", lambda: open_testa_ui(self)),
            ("Tabela: Possui (Editores-Receitas)", lambda: open_possui_ui(self))
        ]

        # Título para tabelas principais
        tk.Label(
            self.scrollable_frame,
            text="Tabelas Principais",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR
        ).grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="w")

        # Botões para tabelas principais
        for i, (text, command) in enumerate(main_tables):
            btn = self.create_button(text, command, BTN_COLOR)
            btn.grid(row=(i // 2) + 1, column=i % 2, padx=20, pady=10)

        # Título para tabelas de relacionamento
        tk.Label(
            self.scrollable_frame,
            text="Tabelas de Relacionamento",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR
        ).grid(row=10, column=0, columnspan=2, pady=(20, 5), sticky="w")

        # Botões para tabelas de relacionamento
        for i, (text, command) in enumerate(rel_tables):
            btn = self.create_button(text, command, BTN_REL_COLOR)
            btn.grid(row=11 + (i // 2), column=i % 2, padx=20, pady=10)

    def create_button(self, text, command, bg_color):
        btn = tk.Button(
            self.scrollable_frame,
            text=text,
            width=30,
            height=2,
            bg=bg_color,
            fg=BTN_TEXT_COLOR,
            bd=0,
            activebackground=BTN_HOVER,
            activeforeground=BTN_TEXT_COLOR,
            font=("Segoe UI", 10, "bold"),
            command=command
        )
        btn.bind("<Enter>", self.on_enter)
        btn.bind("<Leave>", self.on_leave)
        return btn

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
