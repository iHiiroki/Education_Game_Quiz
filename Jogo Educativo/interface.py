
"""
Interface gráfica do RPG Educativo
"""

import tkinter as tk
from tkinter import ttk
from config import CORES, TEMAS_DISPONIVEIS, CONFIGURACOES_PADRAO, JANELA_CONFIG, DIFICULDADES
from utils import (limpar_tela, centralizar_janela, criar_botao_moderno, mostrar_popup, 
                  mostrar_popup_questao, configurar_placeholder, configurar_placeholder_text,
                  configurar_scroll_mouse, bind_scroll_to_children, rolar_dado)
from perguntas import GerenciadorPerguntas, PerguntaDialogModerno
from jogo import LogicaJogo
from resultado import TelaResultados

class JogoEducativoRPG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(JANELA_CONFIG["titulo"])
        self.root.geometry(JANELA_CONFIG["geometria"])
        self.root.configure(bg=CORES["bg_primary"])
        self.fullscreen = False
        
        # Maximizar janela de forma compatível
        try:
            # Para Windows
            self.root.state('zoomed')
        except:
            try:
                # Para Linux/Unix
                self.root.attributes('-zoomed', True)
            except:
                # Fallback: usar geometria da tela
                try:
                    width = self.root.winfo_screenwidth()
                    height = self.root.winfo_screenheight()
                    self.root.geometry(f"{width}x{height}+0+0")
                except:
                    pass
        
        self._configurar_fullscreen()

        self.configuracoes = CONFIGURACOES_PADRAO.copy()
        self.tema_selecionado = "Personalizado"
        
        # Inicializar componentes
        self.gerenciador_perguntas = GerenciadorPerguntas()
        self.logica_jogo = LogicaJogo(self.gerenciador_perguntas, self.configuracoes)
        
        self._configurar_estilos()
        self.criar_menu_principal()

    def _configurar_fullscreen(self):
        def toggle_fullscreen(event=None):
            try:
                self.fullscreen = not self.fullscreen
                self.root.attributes("-fullscreen", self.fullscreen)
                if self.fullscreen:
                    self.root.title(f"{JANELA_CONFIG['titulo']} [TELA CHEIA - ESC para sair]")
                else:
                    self.root.title(JANELA_CONFIG["titulo"])
                    self.root.geometry(JANELA_CONFIG["geometria"])
                    centralizar_janela(self.root)
                return "break"
            except Exception as e:
                print(f"Erro ao alternar tela cheia: {e}")

        def exit_fullscreen(event=None):
            try:
                if self.fullscreen:
                    self.fullscreen = False
                    self.root.attributes("-fullscreen", False)
                    self.root.title(JANELA_CONFIG["titulo"])
                    self.root.geometry(JANELA_CONFIG["geometria"])
                    centralizar_janela(self.root)
                return "break"
            except Exception as e:
                print(f"Erro ao sair da tela cheia: {e}")

        self.root.bind("<F11>", toggle_fullscreen)
        self.root.bind("<Escape>", exit_fullscreen)
        self.root.focus_set()

    def _configurar_estilos(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
            self.style.configure('Title.TLabel', 
                               font=('Segoe UI', 28, 'bold'),
                               background=CORES["bg_primary"],
                               foreground=CORES["accent_blue"])

            self.style.configure('Subtitle.TLabel',
                               font=('Segoe UI', 14),
                               background=CORES["bg_primary"],
                               foreground=CORES["text_secondary"])

            self.style.configure('Modern.TButton',
                               font=('Segoe UI', 12, 'bold'),
                               padding=(20, 15))
        except:
            pass

    def criar_menu_principal(self):
        limpar_tela(self.root)
        main_frame = tk.Frame(self.root, bg=CORES["bg_primary"])
        main_frame.pack(expand=True, fill='both')

        header_frame = tk.Frame(main_frame, bg=CORES["bg_primary"], height=220)
        header_frame.pack(fill='x', pady=60)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🎲 RPG EDUCATIVO 🎲", font=('Segoe UI', 36, 'bold'),
                bg=CORES["bg_primary"], fg=CORES["accent_blue"]).pack(pady=25)
        tk.Label(header_frame, text="✨ Aventura do Conhecimento ✨", font=('Segoe UI', 18),
                bg=CORES["bg_primary"], fg=CORES["text_secondary"]).pack(pady=15)

        botoes_frame = tk.Frame(main_frame, bg=CORES["bg_primary"])
        botoes_frame.pack(expand=True, pady=35)

        criar_botao_moderno(botoes_frame, "🎯 COMEÇAR AVENTURA", self.menu_configurar_perguntas, CORES["accent_green"]).pack(pady=25, padx=60)
        criar_botao_moderno(botoes_frame, "⚙️ CONFIGURAÇÕES", self.menu_opcoes, CORES["accent_blue"]).pack(pady=25, padx=60)
        criar_botao_moderno(botoes_frame, "🚪 SAIR", self.sair_jogo, CORES["accent_red"]).pack(pady=25, padx=60)

        # Frame inferior com dica e créditos
        footer_frame = tk.Frame(main_frame, bg=CORES["bg_primary"])
        footer_frame.pack(side='bottom', fill='x', pady=20)
        
        # Dica sobre teclas (centralizada)
        tk.Label(footer_frame, text="💡 Dica: Pressione F11 para Tela Cheia • ESC para sair da Tela Cheia", 
                font=('Segoe UI', 12), bg=CORES["bg_primary"], fg=CORES["text_secondary"]).pack()
        
        # Créditos (canto inferior direito, mas com margem)
        creditos_frame = tk.Frame(footer_frame, bg=CORES["bg_primary"])
        creditos_frame.pack(side='right', anchor='se', padx=50)
        
        tk.Label(creditos_frame, text="Feito por Daniel Crispino e Rafael da Silva Rodrigues", 
                font=('Segoe UI', 10), bg=CORES["bg_primary"], fg=CORES["text_secondary"]).pack()

    def menu_opcoes(self):
        limpar_tela(self.root)
        main_frame = tk.Frame(self.root, bg=CORES["bg_secondary"])
        main_frame.pack(expand=True, fill='both', padx=35, pady=35)

        tk.Label(main_frame, text="⚙️ CONFIGURAÇÕES AVANÇADAS", font=('Segoe UI', 26, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["accent_blue"]).pack(pady=35)

        opcoes_container = tk.Frame(main_frame, bg=CORES["bg_accent"], relief='solid', bd=2)
        opcoes_container.pack(fill='x', pady=25, padx=25)

        # Opção dicas
        opcao_frame1 = tk.Frame(opcoes_container, bg=CORES["bg_accent"])
        opcao_frame1.pack(pady=35, fill='x', padx=35)
        tk.Label(opcao_frame1, text="💡 Sistema de Dicas:", font=('Segoe UI', 18, 'bold'), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(anchor='w')
        self.dicas_ativadas_var = tk.BooleanVar(value=self.configuracoes["dicas_ativadas"])
        tk.Checkbutton(opcao_frame1, text="Ativar dicas durante o jogo", variable=self.dicas_ativadas_var,
                      bg=CORES["bg_accent"], fg=CORES["text_primary"], font=('Segoe UI', 14), 
                      selectcolor=CORES["accent_green"], activebackground=CORES["bg_accent"]).pack(anchor='w', padx=25, pady=12)

        # Opção tentativas
        opcao_frame2 = tk.Frame(opcoes_container, bg=CORES["bg_accent"])
        opcao_frame2.pack(pady=35, fill='x', padx=35)
        tk.Label(opcao_frame2, text="🎯 Tentativas por Pergunta:", font=('Segoe UI', 18, 'bold'),
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(anchor='w')
        self.num_tentativas_var = tk.IntVar(value=self.configuracoes["num_tentativas"])
        tk.Spinbox(opcao_frame2, from_=1, to=5, textvariable=self.num_tentativas_var,
                  font=('Segoe UI', 16), width=12, bg=CORES["text_primary"]).pack(anchor='w', padx=25, pady=12)

        # Opção ordem aleatória
        opcao_frame3 = tk.Frame(opcoes_container, bg=CORES["bg_accent"])
        opcao_frame3.pack(pady=35, fill='x', padx=35)
        tk.Label(opcao_frame3, text="🔀 Ordem das Perguntas:", font=('Segoe UI', 18, 'bold'), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(anchor='w')
        self.ordem_aleatoria_var = tk.BooleanVar(value=self.configuracoes["ordem_aleatoria"])
        tk.Checkbutton(opcao_frame3, text="Embaralhar perguntas (ordem aleatória)", variable=self.ordem_aleatoria_var,
                      bg=CORES["bg_accent"], fg=CORES["text_primary"], font=('Segoe UI', 14), 
                      selectcolor=CORES["accent_green"], activebackground=CORES["bg_accent"]).pack(anchor='w', padx=25, pady=12)

        botoes_frame = tk.Frame(main_frame, bg=CORES["bg_secondary"])
        botoes_frame.pack(pady=45)
        criar_botao_moderno(botoes_frame, "💾 SALVAR CONFIGURAÇÕES", self.salvar_configuracoes, CORES["accent_green"]).pack(side='left', padx=18)
        criar_botao_moderno(botoes_frame, "↩️ VOLTAR AO MENU", self.criar_menu_principal, CORES["accent_blue"]).pack(side='left', padx=18)

    def salvar_configuracoes(self):
        self.configuracoes["dicas_ativadas"] = self.dicas_ativadas_var.get()
        self.configuracoes["num_tentativas"] = self.num_tentativas_var.get()
        self.configuracoes["ordem_aleatoria"] = self.ordem_aleatoria_var.get()
        
        # Atualizar configurações na lógica do jogo
        self.logica_jogo.configuracoes = self.configuracoes
        
        mostrar_popup(self.root, "✅ Sucesso", "Configurações salvas com sucesso!", "success")
        self.criar_menu_principal()

    def menu_configurar_perguntas(self):
        limpar_tela(self.root)
        main_frame = tk.Frame(self.root, bg=CORES["bg_primary"])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        header_frame = tk.Frame(main_frame, bg=CORES["accent_yellow"], height=60)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=CORES["accent_yellow"])
        header_content.pack(expand=True, fill='both', padx=20, pady=15)

        tk.Label(header_content, text="🎮 Criar Novo Jogo Educativo", 
                font=('Segoe UI', 20, 'bold'),
                bg=CORES["accent_yellow"], fg="#2c3e50").pack(side='left')

        container = tk.Frame(main_frame, bg=CORES["bg_card"])
        container.pack(expand=True, fill='both')

        # Painel esquerdo
        left_panel = tk.Frame(container, bg=CORES["bg_card"], width=400)
        left_panel.pack(side='left', fill='both', expand=True, padx=(30, 15), pady=30)
        left_panel.pack_propagate(False)

        perguntas_header = tk.Frame(left_panel, bg=CORES["bg_card"])
        perguntas_header.pack(fill='x', pady=(0, 15))

        tk.Label(perguntas_header, text="❓ Lista de Perguntas", 
                font=('Segoe UI', 16, 'bold'),
                bg=CORES["bg_card"], fg=CORES["text_primary"]).pack(side='left')

        btn_adicionar = tk.Button(perguntas_header, text="+ Nova",
                                 command=self.adicionar_pergunta,
                                 font=('Segoe UI', 11, 'bold'),
                                 bg=CORES["accent_blue"], fg="white",
                                 relief='flat', padx=15, pady=8, cursor='hand2',
                                 activebackground="#5dade2", activeforeground="white")
        btn_adicionar.pack(side='right')

        # Efeitos hover
        btn_adicionar.bind("<Enter>", lambda e: btn_adicionar.configure(bg="#5dade2"))
        btn_adicionar.bind("<Leave>", lambda e: btn_adicionar.configure(bg=CORES["accent_blue"]))

        self.criar_lista_perguntas(left_panel)

        # Painel direito
        right_panel = tk.Frame(container, bg=CORES["bg_secondary"], relief='solid', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(15, 30), pady=30)

        tk.Label(right_panel, text="⚙️ CONFIGURAÇÕES DO JOGO", font=('Segoe UI', 16, 'bold'),
                bg=CORES["accent_blue"], fg="white").pack(fill='x', pady=15)

        self.criar_painel_configuracoes(right_panel)

        botoes_frame = tk.Frame(main_frame, bg=CORES["bg_primary"])
        botoes_frame.pack(pady=20)
        criar_botao_moderno(botoes_frame, "🚀 INICIAR AVENTURA", self.iniciar_jogo, CORES["accent_blue"]).pack(side='left', padx=8)
        criar_botao_moderno(botoes_frame, "↩️ VOLTAR", self.criar_menu_principal, CORES["accent_orange"]).pack(side='left', padx=8)

    def criar_painel_configuracoes(self, parent):
        canvas = tk.Canvas(parent, bg=CORES["bg_secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        config_frame = tk.Frame(canvas, bg=CORES["bg_secondary"])

        config_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=config_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_functions = configurar_scroll_mouse(canvas)

        config_frame.bind("<Configure>", 
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), 
                      bind_scroll_to_children(config_frame, scroll_functions)])
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)

        # Título
        tk.Label(config_frame, text="📝 Título do Jogo *", font=('Segoe UI', 14, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w', pady=(15, 5))
        self.titulo_entry = tk.Entry(config_frame, font=('Segoe UI', 12),
                                    bg=CORES["bg_input"], fg=CORES["text_secondary"],
                                    relief='flat', bd=10, insertbackground=CORES["text_primary"])
        self.titulo_entry.pack(fill='x', pady=(0, 20))
        configurar_placeholder(self.titulo_entry, "Ex: Quiz de Matemática", CORES)

        # Tema
        tk.Label(config_frame, text="🏷️ Tema *", font=('Segoe UI', 14, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w', pady=(0, 5))
        self.tema_var = tk.StringVar(value=self.tema_selecionado)
        self.tema_combo = ttk.Combobox(config_frame, textvariable=self.tema_var, values=TEMAS_DISPONIVEIS, 
                                      font=('Segoe UI', 12), state="readonly")
        self.tema_combo.pack(fill='x', pady=(0, 20))
        self.tema_combo.bind("<<ComboboxSelected>>", self.on_tema_change)

        # Descrição
        tk.Label(config_frame, text="📄 Descrição", 
                font=('Segoe UI', 14, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w', pady=(0, 5))

        self.desc_text = tk.Text(config_frame, height=4, font=('Segoe UI', 12),
                                bg=CORES["bg_input"], fg=CORES["text_secondary"],
                                relief='flat', bd=10, insertbackground=CORES["text_primary"])
        self.desc_text.pack(fill='x', pady=(0, 20))
        configurar_placeholder_text(self.desc_text, "Descreva brevemente sobre o que é este jogo educativo...", CORES)
        
        # Configurações extras
        self.criar_configuracoes_extras(config_frame)

    def on_tema_change(self, event):
        """Handler para mudança de tema"""
        if self.tema_var.get() == "Personalizado":
            self.tema_combo.config(state="normal")
            self.tema_combo.delete(0, tk.END)
            self.tema_combo.focus()
        else:
            self.tema_combo.config(state="readonly")

    def criar_configuracoes_extras(self, parent):
        """Configurações adicionais"""
        tk.Label(parent, text="🎮 Configurações Extras", 
                font=('Segoe UI', 14, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["accent_yellow"]).pack(anchor='w', pady=(10, 10))

        # Número de tentativas padrão
        tk.Label(parent, text="🎯 Tentativas por Pergunta:", 
                font=('Segoe UI', 12),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w', pady=(0, 5))

        self.tentativas_jogo_var = tk.IntVar(value=2)
        tentativas_spin = tk.Spinbox(parent, from_=1, to=5, textvariable=self.tentativas_jogo_var,
                                   font=('Segoe UI', 12), bg=CORES["text_primary"])
        tentativas_spin.pack(fill='x', pady=(0, 15))

        # Dicas ativadas por padrão
        self.dicas_jogo_var = tk.BooleanVar(value=True)
        dicas_check = tk.Checkbutton(parent, text="💡 Ativar dicas por padrão", 
                                   variable=self.dicas_jogo_var,
                                   bg=CORES["bg_secondary"], fg=CORES["text_primary"], 
                                   font=('Segoe UI', 12), selectcolor=CORES["accent_green"],
                                   activebackground=CORES["bg_secondary"])
        dicas_check.pack(anchor='w', pady=(0, 20))

    def criar_lista_perguntas(self, parent):
        lista_frame = tk.Frame(parent, bg=CORES["bg_input"], relief='solid', bd=1)
        lista_frame.pack(expand=True, fill='both')

        canvas = tk.Canvas(lista_frame, bg=CORES["bg_input"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=CORES["bg_input"])

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_functions = configurar_scroll_mouse(canvas)

        self.scrollable_frame.bind("<Configure>", 
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), 
                      bind_scroll_to_children(self.scrollable_frame, scroll_functions)])

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas_perguntas = canvas
        self.atualizar_lista_perguntas()

    def atualizar_lista_perguntas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if self.gerenciador_perguntas.total_perguntas() == 0:
            tk.Label(self.scrollable_frame, text="Nenhuma pergunta adicionada ainda.\nClique em '+ Nova' para começar!",
                    font=('Segoe UI', 14), bg=CORES["bg_input"], fg=CORES["text_secondary"],
                    justify='center').pack(expand=True, pady=50)
        else:
            for i, pergunta in enumerate(self.gerenciador_perguntas.perguntas):
                self.criar_item_pergunta(i, pergunta)

        self.scrollable_frame.update_idletasks()
        self.canvas_perguntas.configure(scrollregion=self.canvas_perguntas.bbox("all"))

    def criar_item_pergunta(self, index, pergunta_data):
        item_frame = tk.Frame(self.scrollable_frame, bg=CORES["bg_secondary"], relief='solid', bd=1)
        item_frame.pack(fill='x', padx=15, pady=8)

        header = tk.Frame(item_frame, bg=CORES["accent_blue"])
        header.pack(fill='x')

        tk.Label(header, text=f"Pergunta {index + 1}", font=('Segoe UI', 14, 'bold'),
                bg=CORES["accent_blue"], fg="white").pack(side='left', padx=15, pady=10)

        botoes_header = tk.Frame(header, bg=CORES["accent_blue"])
        botoes_header.pack(side='right', padx=15, pady=8)

        tk.Button(botoes_header, text="✏️", font=('Segoe UI', 14), bg=CORES["accent_yellow"], fg="white",
                 relief='flat', width=4, height=1, command=lambda: self.editar_pergunta_por_indice(index),
                 cursor='hand2').pack(side='left', padx=(0, 5))
        tk.Button(botoes_header, text="🗑️", font=('Segoe UI', 14), bg=CORES["accent_red"], fg="white",
                 relief='flat', width=4, height=1, command=lambda: self.remover_pergunta_por_indice(index),
                 cursor='hand2').pack(side='left')

        content = tk.Frame(item_frame, bg=CORES["bg_secondary"])
        content.pack(fill='x', padx=15, pady=15)

        tk.Label(content, text="Texto da Pergunta *", font=('Segoe UI', 12, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w')
        pergunta_text = tk.Text(content, height=2, font=('Segoe UI', 11), bg=CORES["bg_input"], 
                               fg=CORES["text_primary"], relief='flat', bd=5, state='disabled')
        pergunta_text.pack(fill='x', pady=(5, 15))
        pergunta_text.config(state='normal')
        pergunta_text.insert("1.0", pergunta_data.get("pergunta", ""))
        pergunta_text.config(state='disabled')

        # Row para resposta e dificuldade
        self.criar_row_resposta_dificuldade(content, pergunta_data)

        # Dicas (se houver)
        self.mostrar_dicas_pergunta(content, pergunta_data)

    def criar_row_resposta_dificuldade(self, parent, pergunta_data):
        """Row para resposta e dificuldade"""
        row_resp = tk.Frame(parent, bg=CORES["bg_secondary"])
        row_resp.pack(fill='x', pady=(0, 15))

        # Resposta correta
        resp_frame = tk.Frame(row_resp, bg=CORES["bg_secondary"])
        resp_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))

        tk.Label(resp_frame, text="Resposta Correta *",
                font=('Segoe UI', 12, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w')

        resp_entry = tk.Entry(resp_frame, font=('Segoe UI', 11),
                             bg=CORES["bg_input"], fg=CORES["text_primary"],
                             relief='flat', bd=5, insertbackground=CORES["text_primary"])
        resp_entry.pack(fill='x', pady=(5, 0))
        resp_entry.insert(0, pergunta_data.get("resposta", ""))
        resp_entry.config(state='disabled')

        # Dificuldade
        dif_frame = tk.Frame(row_resp, bg=CORES["bg_secondary"])
        dif_frame.pack(side='right', fill='x', expand=True)

        tk.Label(dif_frame, text="Dificuldade *",
                font=('Segoe UI', 12, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(anchor='w')

        dif_entry = tk.Entry(dif_frame, font=('Segoe UI', 11),
                            bg=CORES["bg_input"], fg=CORES["text_primary"],
                            relief='flat', bd=5, insertbackground=CORES["text_primary"])
        dif_entry.pack(fill='x', pady=(5, 0))

        # Mostrar dificuldade da pergunta
        dificuldade = pergunta_data.get("dificuldade", "medio")
        pontos = pergunta_data.get("pontos", 20)
        dificuldade_texto = {
            "facil": f"Fácil ({pontos} pts)",
            "medio": f"Médio ({pontos} pts)", 
            "dificil": f"Difícil ({pontos} pts)"
        }
        dif_entry.insert(0, dificuldade_texto.get(dificuldade, f"Médio ({pontos} pts)"))
        dif_entry.config(state='disabled')

    def mostrar_dicas_pergunta(self, parent, pergunta_data):
        """Mostrar dicas da pergunta"""
        dicas = pergunta_data.get("dicas", [])
        if dicas:
            dicas_frame = tk.Frame(parent, bg=CORES["bg_secondary"])
            dicas_frame.pack(fill='x', pady=(5, 0))

            tk.Label(dicas_frame, text="💡 Dicas:",
                    font=('Segoe UI', 10, 'bold'),
                    bg=CORES["bg_secondary"], fg=CORES["accent_yellow"]).pack(anchor='w')

            for i, dica in enumerate(dicas, 1):
                if dica.strip():  # Só mostra dicas não vazias
                    tk.Label(dicas_frame, text=f"   {i}. {dica}",
                            font=('Segoe UI', 9),
                            bg=CORES["bg_secondary"], fg=CORES["accent_yellow"]).pack(anchor='w')

    def editar_pergunta_por_indice(self, index):
        try:
            pergunta_atual = self.gerenciador_perguntas.perguntas[index]
            dialog = PerguntaDialogModerno(self.root, pergunta_editada=pergunta_atual)
            if dialog.pergunta and dialog.resposta:
                pergunta_data = {
                    "pergunta": dialog.pergunta,
                    "resposta": dialog.resposta,
                    "dica": dialog.dica,
                    "dicas": getattr(dialog, 'dicas', [dialog.dica] if dialog.dica else []),
                    "dificuldade": getattr(dialog, 'dificuldade', 'medio'),
                    "pontos": getattr(dialog, 'pontos', 20),
                    "tentativas_custom": dialog.tentativas_pergunta,
                    "dicas_custom": dialog.dicas_ativadas_pergunta
                }
                self.gerenciador_perguntas.editar_pergunta(index, pergunta_data)
                self.atualizar_lista_perguntas()
                mostrar_popup(self.root, "✅ Sucesso", "Pergunta editada com sucesso!", "success")
        except:
            mostrar_popup(self.root, "⚠️ Erro", "Pergunta não encontrada!", "error")

    def remover_pergunta_por_indice(self, index):
        try:
            resultado = mostrar_popup_questao(self.root, "🗑️ Remover Pergunta", f"Deseja realmente remover a Pergunta {index + 1}?")
            if resultado:
                self.gerenciador_perguntas.remover_pergunta(index)
                self.atualizar_lista_perguntas()
                mostrar_popup(self.root, "✅ Sucesso", "Pergunta removida com sucesso!", "success")
        except:
            mostrar_popup(self.root, "⚠️ Erro", "Pergunta não encontrada!", "error")

    def adicionar_pergunta(self):
        try:
            dialog = PerguntaDialogModerno(self.root)
            if dialog.pergunta and dialog.resposta:
                pergunta_data = {
                    "pergunta": dialog.pergunta,
                    "resposta": dialog.resposta,
                    "dica": dialog.dica,
                    "dicas": getattr(dialog, 'dicas', [dialog.dica] if dialog.dica else []),
                    "dificuldade": getattr(dialog, 'dificuldade', 'medio'),
                    "pontos": getattr(dialog, 'pontos', 20),
                    "tentativas_custom": dialog.tentativas_pergunta,
                    "dicas_custom": dialog.dicas_ativadas_pergunta
                }
                self.gerenciador_perguntas.adicionar_pergunta(pergunta_data)
                self.atualizar_lista_perguntas()
        except:
            pass

    def iniciar_jogo(self):
        sucesso, mensagem = self.logica_jogo.iniciar_jogo()
        if not sucesso:
            mostrar_popup(self.root, "⚠️ Atenção", mensagem, "warning")
            return
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        if self.logica_jogo.jogo_finalizado():
            self.mostrar_resultado_final()
            return

        limpar_tela(self.root)
        pergunta_config = self.logica_jogo.obter_pergunta_atual()
        self.logica_jogo.inicializar_tentativas()

        main_frame = tk.Frame(self.root, bg=CORES["bg_primary"])
        main_frame.pack(expand=True, fill='both', padx=25, pady=25)

        header_frame = tk.Frame(main_frame, bg=CORES["bg_secondary"], relief='solid', bd=2)
        header_frame.pack(fill='x', pady=12)

        tk.Label(header_frame, text=f"🎲 PERGUNTA {self.logica_jogo.obter_numero_pergunta_atual()} DE {self.logica_jogo.obter_total_perguntas_jogo()}", 
                font=('Segoe UI', 22, 'bold'), bg=CORES["bg_secondary"], fg=CORES["accent_red"]).pack(pady=18)

        status_frame = tk.Frame(header_frame, bg=CORES["bg_secondary"])
        status_frame.pack(pady=12)
        tk.Label(status_frame, text=f"🎯 Tentativas: {self.logica_jogo.tentativas_restantes}", 
                font=('Segoe UI', 16), bg=CORES["bg_secondary"], fg=CORES["accent_orange"]).pack(side='left', padx=25)
        tk.Label(status_frame, text=f"🎲 Sorte: {rolar_dado()}", 
                font=('Segoe UI', 16), bg=CORES["bg_secondary"], fg=CORES["accent_green"]).pack(side='right', padx=25)

        pergunta_frame = tk.Frame(main_frame, bg=CORES["bg_accent"], relief='solid', bd=2)
        pergunta_frame.pack(fill='x', pady=35, padx=25)
        tk.Label(pergunta_frame, text=pergunta_config["pergunta"], font=('Segoe UI', 18), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"], wraplength=850, justify='center').pack(pady=35, padx=25)

        resposta_frame = tk.Frame(main_frame, bg=CORES["bg_primary"])
        resposta_frame.pack(pady=35)
        tk.Label(resposta_frame, text="💭 Sua Resposta:", font=('Segoe UI', 16, 'bold'), 
                bg=CORES["bg_primary"], fg=CORES["text_primary"]).pack(pady=12)

        self.entrada_resposta = tk.Entry(resposta_frame, font=('Segoe UI', 18), width=55, relief='flat', bd=8)
        self.entrada_resposta.pack(pady=18)
        self.entrada_resposta.bind('<Return>', lambda e: self.verificar_resposta())
        self.entrada_resposta.focus()

        botoes_acao = tk.Frame(resposta_frame, bg=CORES["bg_primary"])
        botoes_acao.pack(pady=25)

        if self.logica_jogo.deve_mostrar_dicas():
            criar_botao_moderno(botoes_acao, "💡 SOLICITAR DICA", self.mostrar_dica_aleatoria, CORES["accent_yellow"]).pack(side='left', padx=10)

        criar_botao_moderno(botoes_acao, "✅ CONFIRMAR RESPOSTA", self.verificar_resposta, CORES["accent_green"]).pack(side='left', padx=10)

    def mostrar_dica_aleatoria(self):
        sucesso, mensagem = self.logica_jogo.obter_dica_aleatoria(self.root)

    def verificar_resposta(self):
        try:
            resposta_usuario = self.entrada_resposta.get().strip()
            sucesso, mensagem = self.logica_jogo.verificar_resposta(resposta_usuario, self.root)
            
            if sucesso or self.logica_jogo.tentativas_restantes == 0:
                # Avançar para próxima pergunta ou finalizar
                self.mostrar_pergunta()
            else:
                # Limpar entrada e focar novamente
                self.entrada_resposta.delete(0, tk.END)
                self.entrada_resposta.focus()
                # Atualizar contador de tentativas na tela
                self._atualizar_tentativas_display()
                
        except Exception as e:
            mostrar_popup(self.root, "⚠️ Erro", f"Erro ao verificar resposta: {str(e)}", "error")

    def _atualizar_tentativas_display(self):
        """Atualizar display de tentativas restantes"""
        # Esta função seria implementada para atualizar apenas o contador
        # Por simplicidade, recarregamos a pergunta
        pass

    def mostrar_resultado_final(self):
        limpar_tela(self.root)
        
        tela_resultados = TelaResultados(
            self.root, 
            self.logica_jogo.respostas_usuario,
            self.recomecar_jogo,
            self.criar_menu_principal
        )
        tela_resultados.criar_tela_resultados()

    def recomecar_jogo(self):
        """Reiniciar o jogo"""
        sucesso, mensagem = self.logica_jogo.recomecar_jogo(self.root)
        if sucesso:
            self.mostrar_pergunta()
        else:
            self.criar_menu_principal()

    def sair_jogo(self):
        resultado = mostrar_popup_questao(self.root, "🚪 Sair do Jogo", "Tem certeza que deseja sair da aventura?")
        if resultado:
            self.root.quit()

    def executar(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Erro ao executar o jogo: {e}")