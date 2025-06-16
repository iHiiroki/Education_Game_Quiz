import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
import json
import os

class PopupModerno:
    def __init__(self, parent, titulo, mensagem, tipo="info", callback=None):
        self.callback = callback
        self.resultado = None
        self.popup = tk.Toplevel(parent)
        self.popup.title(titulo)
        self.popup.geometry("450x280")
        self.popup.configure(bg="#2c3e50")
        self.popup.resizable(False, False)
        self.popup.transient(parent)
        self.popup.grab_set()
        self.centralizar_popup(parent)
        self.criar_interface(titulo, mensagem, tipo)
        self.animar_entrada()
        if not callback:
            self.popup.wait_window()

    def centralizar_popup(self, parent):
        try:
            parent.update_idletasks()
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 225
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 140
            self.popup.geometry(f"450x280+{x}+{y}")
        except:
            self.popup.geometry("450x280+400+200")

    def criar_interface(self, titulo, mensagem, tipo):
        main_frame = tk.Frame(self.popup, bg="#34495e", relief='solid', bd=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        title_frame = tk.Frame(main_frame, bg="#2c3e50", height=45)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        icones = {"info": "ℹ️", "success": "✅", "warning": "⚠", "error": "❌", "question": "❓"}
        icone = icones.get(tipo, "ℹ️")

        tk.Label(title_frame, text=f"{icone} {titulo}", font=('Segoe UI', 13, 'bold'),
                bg="#2c3e50", fg="#ecf0f1").pack(side='left', padx=20, pady=12)

        tk.Button(title_frame, text="✕", font=('Segoe UI', 11, 'bold'),
                 bg="#e74c3c", fg="white", relief='flat', width=3, height=1,
                 command=self.fechar).pack(side='right', padx=15, pady=10)

        content_frame = tk.Frame(main_frame, bg="#34495e")
        content_frame.pack(fill='both', expand=True, padx=25, pady=25)

        tk.Label(content_frame, text=mensagem, font=('Segoe UI', 12),
                bg="#34495e", fg="#ecf0f1", wraplength=380, justify='center').pack(pady=25)

        self.criar_botoes(content_frame, tipo)

    def criar_botoes(self, parent, tipo):
        botoes_frame = tk.Frame(parent, bg="#34495e")
        botoes_frame.pack(side='bottom', pady=15)

        if tipo == "question":
            tk.Button(botoes_frame, text="✅ SIM", font=('Segoe UI', 11, 'bold'),
                     bg="#27ae60", fg="white", relief='flat', padx=25, pady=8,
                     command=lambda: self.definir_resultado(True)).pack(side='left', padx=12)
            tk.Button(botoes_frame, text="❌ NÃO", font=('Segoe UI', 11, 'bold'),
                     bg="#e74c3c", fg="white", relief='flat', padx=25, pady=8,
                     command=lambda: self.definir_resultado(False)).pack(side='left', padx=12)
        else:
            tk.Button(botoes_frame, text="✓ OK", font=('Segoe UI', 11, 'bold'),
                     bg="#3498db", fg="white", relief='flat', padx=35, pady=8,
                     command=self.fechar).pack()

    def animar_entrada(self):
        try:
            self.popup.attributes('-alpha', 0.3)
            self.fade_in(0.3)
        except:
            pass

    def fade_in(self, alpha=0.3):
        try:
            alpha += 0.15
            self.popup.attributes('-alpha', alpha)
            if alpha < 1.0:
                self.popup.after(50, lambda: self.fade_in(alpha))
        except:
            pass

    def definir_resultado(self, resultado):
        self.resultado = resultado
        if self.callback:
            self.callback(resultado)
        self.fechar()

    def fechar(self):
        try:
            self.popup.destroy()
        except:
            pass

class JogoEducativoRPG:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RPG Educativo - Aventura do Conhecimento")
        self.root.geometry("1100x800")
        self.root.configure(bg="#1a252f")
        self.fullscreen = False
        self.centralizar_janela()
        self.configurar_fullscreen()

        self.configuracoes = {"dicas_ativadas": True, "num_tentativas": 2, "ordem_aleatoria": False}
        self.reset_dados_jogo()
        self.temas_disponiveis = ["Matemática", "Física", "História", "Geografia", "Ciências", "Literatura", "Inglês", "Personalizado"]
        self.cores = {"bg_primary": "#1a252f", "bg_secondary": "#2c3e50", "bg_accent": "#34495e", "bg_card": "#2d3748", 
                     "bg_input": "#1a202c", "text_primary": "#ecf0f1", "text_secondary": "#bdc3c7", "accent_blue": "#3498db",
                     "accent_green": "#2ecc71", "accent_red": "#e74c3c", "accent_orange": "#f39c12", "accent_purple": "#9b59b6",
                     "accent_yellow": "#f1c40f"}
        self.configurar_estilos()
        self.criar_menu_principal()

    def centralizar_janela(self):
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'{width}x{height}+{x}+{y}')
        except:
            pass

    def configurar_fullscreen(self):
        def toggle_fullscreen(event=None):
            try:
                self.fullscreen = not self.fullscreen
                self.root.attributes("-fullscreen", self.fullscreen)
                if self.fullscreen:
                    self.root.title("RPG Educativo - Aventura do Conhecimento [TELA CHEIA - ESC para sair]")
                else:
                    self.root.title("RPG Educativo - Aventura do Conhecimento")
                    self.root.geometry("1100x800")
                    self.centralizar_janela()
                return "break"
            except Exception as e:
                print(f"Erro ao alternar tela cheia: {e}")

        def exit_fullscreen(event=None):
            try:
                if self.fullscreen:
                    self.fullscreen = False
                    self.root.attributes("-fullscreen", False)
                    self.root.title("RPG Educativo - Aventura do Conhecimento")
                    self.root.geometry("1100x800")
                    self.centralizar_janela()
                return "break"
            except Exception as e:
                print(f"Erro ao sair da tela cheia: {e}")

        self.root.bind("<F11>", toggle_fullscreen)
        self.root.bind("<Escape>", exit_fullscreen)
        self.root.focus_set()

    def reset_dados_jogo(self):
        self.perguntas = []
        self.perguntas_jogo = []
        self.respostas_usuario = []
        self.tentativas_restantes = 0
        self.pergunta_atual = 0
        self.tema_selecionado = "Personalizado"

    def configurar_estilos(self):
        # Cores modernas - OTIMIZADO: dicionário mais organizado
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
            self.style.configure('Title.TLabel', 
                               font=('Segoe UI', 28, 'bold'),
                               background=self.cores["bg_primary"],
                               foreground=self.cores["accent_blue"])

            self.style.configure('Subtitle.TLabel',
                               font=('Segoe UI', 14),
                               background=self.cores["bg_primary"],
                               foreground=self.cores["text_secondary"])

            self.style.configure('Modern.TButton',
                               font=('Segoe UI', 12, 'bold'),
                               padding=(20, 15))
        except:
            pass

    def criar_botao_moderno(self, parent, texto, comando, cor_bg, cor_fg="white"):
        btn = tk.Button(parent, text=texto, command=comando, font=('Segoe UI', 13, 'bold'), 
                       bg=cor_bg, fg=cor_fg, relief='flat', padx=35, pady=18, cursor='hand2')
        cores_hover = {"#3498db": "#5dade2", "#2ecc71": "#58d68d", "#e74c3c": "#ec7063", "#f39c12": "#f8c471", "#9b59b6": "#bb8fce"}
        try:
            btn.bind("<Enter>", lambda e: btn.configure(bg=cores_hover.get(cor_bg, cor_bg)))
            btn.bind("<Leave>", lambda e: btn.configure(bg=cor_bg))
        except:
            pass
        return btn

    def clarear_cor(self, cor):
        """OTIMIZADO: Dicionário de cores hover"""
        cores_hover = {
            "#3498db": "#5dade2",
            "#2ecc71": "#58d68d",
            "#e74c3c": "#ec7063",
            "#f39c12": "#f8c471",
            "#9b59b6": "#bb8fce"
        }
        return cores_hover.get(cor, cor)

    def mostrar_popup(self, titulo, mensagem, tipo="info"):
        try:
            return PopupModerno(self.root, titulo, mensagem, tipo)
        except Exception as e:
            # Fallback para messagebox padrão
            if tipo == "question":
                return messagebox.askyesno(titulo, mensagem)
            elif tipo == "error":
                messagebox.showerror(titulo, mensagem)
            elif tipo == "warning":
                messagebox.showwarning(titulo, mensagem)
            else:
                messagebox.showinfo(titulo, mensagem)

    def mostrar_popup_questao(self, titulo, mensagem):
        try:
            popup = PopupModerno(self.root, titulo, mensagem, "question")
            return popup.resultado
        except:
            return messagebox.askyesno(titulo, mensagem)

    def limpar_tela(self):
        try:
            for widget in self.root.winfo_children():
                widget.destroy()
        except:
            pass

    def criar_menu_principal(self):
        self.limpar_tela()
        main_frame = tk.Frame(self.root, bg=self.cores["bg_primary"])
        main_frame.pack(expand=True, fill='both')

        header_frame = tk.Frame(main_frame, bg=self.cores["bg_primary"], height=220)
        header_frame.pack(fill='x', pady=60)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🎲 RPG EDUCATIVO 🎲", font=('Segoe UI', 36, 'bold'),
                bg=self.cores["bg_primary"], fg=self.cores["accent_blue"]).pack(pady=25)
        tk.Label(header_frame, text="✨ Aventura do Conhecimento ✨", font=('Segoe UI', 18),
                bg=self.cores["bg_primary"], fg=self.cores["text_secondary"]).pack(pady=15)

        botoes_frame = tk.Frame(main_frame, bg=self.cores["bg_primary"])
        botoes_frame.pack(expand=True, pady=35)

        self.criar_botao_moderno(botoes_frame, "🎯 COMEÇAR AVENTURA", self.menu_configurar_perguntas, self.cores["accent_green"]).pack(pady=25, padx=60)
        self.criar_botao_moderno(botoes_frame, "⚙️ CONFIGURAÇÕES", self.menu_opcoes, self.cores["accent_blue"]).pack(pady=25, padx=60)
        self.criar_botao_moderno(botoes_frame, "🚪 SAIR", self.sair_jogo, self.cores["accent_red"]).pack(pady=25, padx=60)

    def menu_opcoes(self):
        self.limpar_tela()
        main_frame = tk.Frame(self.root, bg=self.cores["bg_secondary"])
        main_frame.pack(expand=True, fill='both', padx=35, pady=35)

        tk.Label(main_frame, text="⚙️ CONFIGURAÇÕES AVANÇADAS", font=('Segoe UI', 26, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["accent_blue"]).pack(pady=35)

        opcoes_container = tk.Frame(main_frame, bg=self.cores["bg_accent"], relief='solid', bd=2)
        opcoes_container.pack(fill='x', pady=25, padx=25)

        # Opção dicas
        opcao_frame1 = tk.Frame(opcoes_container, bg=self.cores["bg_accent"])
        opcao_frame1.pack(pady=35, fill='x', padx=35)
        tk.Label(opcao_frame1, text="💡 Sistema de Dicas:", font=('Segoe UI', 18, 'bold'), 
                bg=self.cores["bg_accent"], fg=self.cores["text_primary"]).pack(anchor='w')
        self.dicas_ativadas_var = tk.BooleanVar(value=self.configuracoes["dicas_ativadas"])
        tk.Checkbutton(opcao_frame1, text="Ativar dicas durante o jogo", variable=self.dicas_ativadas_var,
                      bg=self.cores["bg_accent"], fg=self.cores["text_primary"], font=('Segoe UI', 14), 
                      selectcolor=self.cores["accent_green"], activebackground=self.cores["bg_accent"]).pack(anchor='w', padx=25, pady=12)

        # Opção tentativas
        opcao_frame2 = tk.Frame(opcoes_container, bg=self.cores["bg_accent"])
        opcao_frame2.pack(pady=35, fill='x', padx=35)
        tk.Label(opcao_frame2, text="🎯 Tentativas por Pergunta:", font=('Segoe UI', 18, 'bold'),
                bg=self.cores["bg_accent"], fg=self.cores["text_primary"]).pack(anchor='w')
        self.num_tentativas_var = tk.IntVar(value=self.configuracoes["num_tentativas"])
        tk.Spinbox(opcao_frame2, from_=1, to=5, textvariable=self.num_tentativas_var,
                  font=('Segoe UI', 16), width=12, bg=self.cores["text_primary"]).pack(anchor='w', padx=25, pady=12)

        # Opção ordem aleatória
        opcao_frame3 = tk.Frame(opcoes_container, bg=self.cores["bg_accent"])
        opcao_frame3.pack(pady=35, fill='x', padx=35)
        tk.Label(opcao_frame3, text="🔀 Ordem das Perguntas:", font=('Segoe UI', 18, 'bold'), 
                bg=self.cores["bg_accent"], fg=self.cores["text_primary"]).pack(anchor='w')
        self.ordem_aleatoria_var = tk.BooleanVar(value=self.configuracoes["ordem_aleatoria"])
        tk.Checkbutton(opcao_frame3, text="Embaralhar perguntas (ordem aleatória)", variable=self.ordem_aleatoria_var,
                      bg=self.cores["bg_accent"], fg=self.cores["text_primary"], font=('Segoe UI', 14), 
                      selectcolor=self.cores["accent_green"], activebackground=self.cores["bg_accent"]).pack(anchor='w', padx=25, pady=12)

        botoes_frame = tk.Frame(main_frame, bg=self.cores["bg_secondary"])
        botoes_frame.pack(pady=45)
        self.criar_botao_moderno(botoes_frame, "💾 SALVAR CONFIGURAÇÕES", self.salvar_configuracoes, self.cores["accent_green"]).pack(side='left', padx=18)
        self.criar_botao_moderno(botoes_frame, "↩️ VOLTAR AO MENU", self.criar_menu_principal, self.cores["accent_blue"]).pack(side='left', padx=18)

    def criar_opcao_checkbox(self, parent, titulo, texto, config_key):
        """OTIMIZADO: Factory method para checkbox options"""
        opcao_frame = tk.Frame(parent, bg=self.cores["bg_accent"])
        opcao_frame.pack(pady=35, fill='x', padx=35)

        tk.Label(opcao_frame, text=titulo, font=('Segoe UI', 18, 'bold'), 
                bg=self.cores["bg_accent"], fg=self.cores["text_primary"]).pack(anchor='w')

        var = tk.BooleanVar(value=self.configuracoes[config_key])
        setattr(self, f"{config_key}_var", var)
        
        check = tk.Checkbutton(opcao_frame, text=texto, variable=var,
                              bg=self.cores["bg_accent"], fg=self.cores["text_primary"], 
                              font=('Segoe UI', 14), selectcolor=self.cores["accent_green"],
                              activebackground=self.cores["bg_accent"])
        check.pack(anchor='w', padx=25, pady=12)

    def criar_opcao_spinbox(self, parent, titulo, config_key, min_val, max_val):
        """OTIMIZADO: Factory method para spinbox options"""
        opcao_frame = tk.Frame(parent, bg=self.cores["bg_accent"])
        opcao_frame.pack(pady=35, fill='x', padx=35)

        tk.Label(opcao_frame, text=titulo, font=('Segoe UI', 18, 'bold'),
                bg=self.cores["bg_accent"], fg=self.cores["text_primary"]).pack(anchor='w')

        var = tk.IntVar(value=self.configuracoes[config_key])
        setattr(self, f"{config_key}_var", var)
        
        spin = tk.Spinbox(opcao_frame, from_=min_val, to=max_val, textvariable=var,
                         font=('Segoe UI', 16), width=12, bg=self.cores["text_primary"])
        spin.pack(anchor='w', padx=25, pady=12)

    def salvar_configuracoes(self):
        self.configuracoes["dicas_ativadas"] = self.dicas_ativadas_var.get()
        self.configuracoes["num_tentativas"] = self.num_tentativas_var.get()
        self.configuracoes["ordem_aleatoria"] = self.ordem_aleatoria_var.get()
        self.mostrar_popup("✅ Sucesso", "Configurações salvas com sucesso!", "success")
        self.criar_menu_principal()

    def menu_configurar_perguntas(self):
        self.limpar_tela()
        main_frame = tk.Frame(self.root, bg=self.cores["bg_primary"])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        header_frame = tk.Frame(main_frame, bg=self.cores["accent_yellow"], height=60)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=self.cores["accent_yellow"])
        header_content.pack(expand=True, fill='both', padx=20, pady=15)

        tk.Label(header_content, text="🎮 Criar Novo Jogo Educativo", 
                font=('Segoe UI', 20, 'bold'),
                bg=self.cores["accent_yellow"], fg="#2c3e50").pack(side='left')

        container = tk.Frame(main_frame, bg=self.cores["bg_card"])
        container.pack(expand=True, fill='both')

        # Painel esquerdo
        left_panel = tk.Frame(container, bg=self.cores["bg_card"], width=400)
        left_panel.pack(side='left', fill='both', expand=True, padx=(30, 15), pady=30)
        left_panel.pack_propagate(False)

        perguntas_header = tk.Frame(left_panel, bg=self.cores["bg_card"])
        perguntas_header.pack(fill='x', pady=(0, 15))

        tk.Label(perguntas_header, text="❓ Lista de Perguntas", 
                font=('Segoe UI', 16, 'bold'),
                bg=self.cores["bg_card"], fg=self.cores["text_primary"]).pack(side='left')

        btn_adicionar = tk.Button(perguntas_header, text="+ Nova",
                                 command=self.adicionar_pergunta,
                                 font=('Segoe UI', 11, 'bold'),
                                 bg="#3498db", fg="white",
                                 relief='flat', padx=15, pady=8, cursor='hand2',
                                 activebackground="#5dade2", activeforeground="white")
        btn_adicionar.pack(side='right')

        # Efeitos hover
        btn_adicionar.bind("<Enter>", lambda e: btn_adicionar.configure(bg="#5dade2"))
        btn_adicionar.bind("<Leave>", lambda e: btn_adicionar.configure(bg="#3498db"))

        self.criar_lista_perguntas(left_panel)

        # Painel direito
        right_panel = tk.Frame(container, bg=self.cores["bg_secondary"], relief='solid', bd=2)
        right_panel.pack(side='right', fill='both', expand=True, padx=(15, 30), pady=30)

        tk.Label(right_panel, text="⚙️ CONFIGURAÇÕES DO JOGO", font=('Segoe UI', 16, 'bold'),
                bg=self.cores["accent_blue"], fg="white").pack(fill='x', pady=15)

        self.criar_painel_configuracoes(right_panel)

        botoes_frame = tk.Frame(main_frame, bg=self.cores["bg_primary"])
        botoes_frame.pack(pady=20)
        self.criar_botao_moderno(botoes_frame, "🚀 INICIAR AVENTURA", self.iniciar_jogo, self.cores["accent_blue"]).pack(side='left', padx=8)
        self.criar_botao_moderno(botoes_frame, "↩️ VOLTAR", self.criar_menu_principal, self.cores["accent_orange"]).pack(side='left', padx=8)

    def criar_painel_configuracoes(self, parent):
        canvas = tk.Canvas(parent, bg=self.cores["bg_secondary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        config_frame = tk.Frame(canvas, bg=self.cores["bg_secondary"])

        config_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=config_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_config_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass

        def on_config_mousewheel_linux_up(event):
            try:
                canvas.yview_scroll(-1, "units")
            except:
                pass

        def on_config_mousewheel_linux_down(event):
            try:
                canvas.yview_scroll(1, "units")
            except:
                pass
        # Bind do scroll do mouse
        canvas.bind("<MouseWheel>", on_config_mousewheel)
        canvas.bind("<Button-4>", on_config_mousewheel_linux_up)
        canvas.bind("<Button-5>", on_config_mousewheel_linux_down)

        # Bind para widgets filhos
        def bind_config_scroll_to_children(widget):
            try:
                widget.bind("<MouseWheel>", on_config_mousewheel)
                widget.bind("<Button-4>", on_config_mousewheel_linux_up)
                widget.bind("<Button-5>", on_config_mousewheel_linux_down)
                for child in widget.winfo_children():
                    bind_config_scroll_to_children(child)
            except:
                pass

        config_frame.bind("<Configure>", 
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), 
                      bind_config_scroll_to_children(config_frame)])
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)

        # Título
        tk.Label(config_frame, text="📝 Título do Jogo *", font=('Segoe UI', 14, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w', pady=(15, 5))
        self.titulo_entry = tk.Entry(config_frame, font=('Segoe UI', 12),
                                    bg=self.cores["bg_input"], fg=self.cores["text_secondary"],
                                    relief='flat', bd=10, insertbackground=self.cores["text_primary"])
        self.titulo_entry.pack(fill='x', pady=(0, 20))
        self.configurar_placeholder(self.titulo_entry, "Ex: Quiz de Matemática")

        # Tema
        tk.Label(config_frame, text="🏷️ Tema *", font=('Segoe UI', 14, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w', pady=(0, 5))
        self.tema_var = tk.StringVar(value=self.tema_selecionado)
        self.tema_combo = ttk.Combobox(config_frame, textvariable=self.tema_var, values=self.temas_disponiveis, 
                                      font=('Segoe UI', 12), state="readonly")
        self.tema_combo.pack(fill='x', pady=(0, 20))
        self.tema_combo.bind("<<ComboboxSelected>>", self.on_tema_change)

        # Descrição
        tk.Label(config_frame, text="📄 Descrição", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w', pady=(0, 5))

        self.desc_text = tk.Text(config_frame, height=4, font=('Segoe UI', 12),
                                bg=self.cores["bg_input"], fg=self.cores["text_secondary"],
                                relief='flat', bd=10, insertbackground=self.cores["text_primary"])
        self.desc_text.pack(fill='x', pady=(0, 20))
        self.configurar_placeholder_text(self.desc_text, "Descreva brevemente sobre o que é este jogo educativo...")
        # Configurações extras
        self.criar_configuracoes_extras(config_frame)

    def configurar_placeholder(self, entry, placeholder):
        """OTIMIZADO: Configuração de placeholder para Entry"""
        entry.insert(0, placeholder)
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.cores["text_primary"])

        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=self.cores["text_secondary"])

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def configurar_placeholder_text(self, text_widget, placeholder):
        """OTIMIZADO: Configuração de placeholder para Text"""
        text_widget.insert("1.0", placeholder)
        
        def on_focus_in(event):
            content = text_widget.get("1.0", tk.END).strip()
            if content == placeholder:
                text_widget.delete("1.0", tk.END)
                text_widget.config(fg=self.cores["text_primary"])

        def on_focus_out(event):
            content = text_widget.get("1.0", tk.END).strip()
            if not content:
                text_widget.insert("1.0", placeholder)
                text_widget.config(fg=self.cores["text_secondary"])

        text_widget.bind("<FocusIn>", on_focus_in)
        text_widget.bind("<FocusOut>", on_focus_out)

    def on_tema_change(self, event):
        """OTIMIZADO: Handler para mudança de tema"""
        if self.tema_var.get() == "Personalizado":
            self.tema_combo.config(state="normal")
            self.tema_combo.delete(0, tk.END)
            self.tema_combo.focus()
        else:
            self.tema_combo.config(state="readonly")

    def criar_configuracoes_extras(self, parent):
        """OTIMIZADO: Configurações adicionais"""
        tk.Label(parent, text="🎮 Configurações Extras", 
                font=('Segoe UI', 14, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["accent_yellow"]).pack(anchor='w', pady=(10, 10))

        # Número de tentativas padrão
        tk.Label(parent, text="🎯 Tentativas por Pergunta:", 
                font=('Segoe UI', 12),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w', pady=(0, 5))

        self.tentativas_jogo_var = tk.IntVar(value=2)
        tentativas_spin = tk.Spinbox(parent, from_=1, to=5, textvariable=self.tentativas_jogo_var,
                                   font=('Segoe UI', 12), bg=self.cores["text_primary"])
        tentativas_spin.pack(fill='x', pady=(0, 15))

        # Dicas ativadas por padrão
        self.dicas_jogo_var = tk.BooleanVar(value=True)
        dicas_check = tk.Checkbutton(parent, text="💡 Ativar dicas por padrão", 
                                   variable=self.dicas_jogo_var,
                                   bg=self.cores["bg_secondary"], fg=self.cores["text_primary"], 
                                   font=('Segoe UI', 12), selectcolor=self.cores["accent_green"],
                                   activebackground=self.cores["bg_secondary"])
        dicas_check.pack(anchor='w', pady=(0, 20))

    def criar_lista_perguntas(self, parent):
        lista_frame = tk.Frame(parent, bg=self.cores["bg_input"], relief='solid', bd=1)
        lista_frame.pack(expand=True, fill='both')

        canvas = tk.Canvas(lista_frame, bg=self.cores["bg_input"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.cores["bg_input"])

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass

        def on_mousewheel_linux_up(event):
            try:
                canvas.yview_scroll(-1, "units")
            except:
                pass

        def on_mousewheel_linux_down(event):
            try:
                canvas.yview_scroll(1, "units")
            except:
                pass

        # Bind do scroll do mouse
        canvas.bind("<MouseWheel>", on_mousewheel)
        canvas.bind("<Button-4>", on_mousewheel_linux_up)
        canvas.bind("<Button-5>", on_mousewheel_linux_down)

        # Bind para todos os widgets filhos também
        def bind_scroll_to_children(widget):
            try:
                widget.bind("<MouseWheel>", on_mousewheel)
                widget.bind("<Button-4>", on_mousewheel_linux_up)
                widget.bind("<Button-5>", on_mousewheel_linux_down)
                for child in widget.winfo_children():
                    bind_scroll_to_children(child)
            except:
                pass

        self.scrollable_frame.bind("<Configure>", 
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), 
                      bind_scroll_to_children(self.scrollable_frame)])

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas_perguntas = canvas
        self.atualizar_lista_perguntas()

    def atualizar_lista_perguntas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.perguntas:
            tk.Label(self.scrollable_frame, text="Nenhuma pergunta adicionada ainda.\nClique em '+ Nova' para começar!",
                    font=('Segoe UI', 14), bg=self.cores["bg_input"], fg=self.cores["text_secondary"],
                    justify='center').pack(expand=True, pady=50)
        else:
            for i, pergunta in enumerate(self.perguntas):
                self.criar_item_pergunta(i, pergunta)

        self.scrollable_frame.update_idletasks()
        self.canvas_perguntas.configure(scrollregion=self.canvas_perguntas.bbox("all"))

    def criar_item_pergunta(self, index, pergunta_data):
        item_frame = tk.Frame(self.scrollable_frame, bg=self.cores["bg_secondary"], relief='solid', bd=1)
        item_frame.pack(fill='x', padx=15, pady=8)

        header = tk.Frame(item_frame, bg=self.cores["accent_blue"])
        header.pack(fill='x')

        tk.Label(header, text=f"Pergunta {index + 1}", font=('Segoe UI', 14, 'bold'),
                bg=self.cores["accent_blue"], fg="white").pack(side='left', padx=15, pady=10)

        botoes_header = tk.Frame(header, bg=self.cores["accent_blue"])
        botoes_header.pack(side='right', padx=15, pady=8)

        tk.Button(botoes_header, text="✏️", font=('Segoe UI', 14), bg=self.cores["accent_yellow"], fg="white",
                 relief='flat', width=4, height=1, command=lambda: self.editar_pergunta_por_indice(index),
                 cursor='hand2').pack(side='left', padx=(0, 5))
        tk.Button(botoes_header, text="🗑️", font=('Segoe UI', 14), bg=self.cores["accent_red"], fg="white",
                 relief='flat', width=4, height=1, command=lambda: self.remover_pergunta_por_indice(index),
                 cursor='hand2').pack(side='left')

        content = tk.Frame(item_frame, bg=self.cores["bg_secondary"])
        content.pack(fill='x', padx=15, pady=15)

        tk.Label(content, text="Texto da Pergunta *", font=('Segoe UI', 12, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w')
        pergunta_text = tk.Text(content, height=2, font=('Segoe UI', 11), bg=self.cores["bg_input"], 
                               fg=self.cores["text_primary"], relief='flat', bd=5, state='disabled')
        pergunta_text.pack(fill='x', pady=(5, 15))
        pergunta_text.config(state='normal')
        pergunta_text.insert("1.0", pergunta_data.get("pergunta", ""))
        pergunta_text.config(state='disabled')

        # Row para resposta e dificuldade
        self.criar_row_resposta_dificuldade(content, pergunta_data)

        # Dicas (se houver)
        self.mostrar_dicas_pergunta(content, pergunta_data)

    def criar_row_resposta_dificuldade(self, parent, pergunta_data):
        """OTIMIZADO: Row para resposta e dificuldade"""
        row_resp = tk.Frame(parent, bg=self.cores["bg_secondary"])
        row_resp.pack(fill='x', pady=(0, 15))

        # Resposta correta
        resp_frame = tk.Frame(row_resp, bg=self.cores["bg_secondary"])
        resp_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))

        tk.Label(resp_frame, text="Resposta Correta *",
                font=('Segoe UI', 12, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w')

        resp_entry = tk.Entry(resp_frame, font=('Segoe UI', 11),
                             bg=self.cores["bg_input"], fg=self.cores["text_primary"],
                             relief='flat', bd=5, insertbackground=self.cores["text_primary"])
        resp_entry.pack(fill='x', pady=(5, 0))
        resp_entry.insert(0, pergunta_data.get("resposta", ""))
        resp_entry.config(state='disabled')

        # Dificuldade
        dif_frame = tk.Frame(row_resp, bg=self.cores["bg_secondary"])
        dif_frame.pack(side='right', fill='x', expand=True)

        tk.Label(dif_frame, text="Dificuldade *",
                font=('Segoe UI', 12, 'bold'),
                bg=self.cores["bg_secondary"], fg=self.cores["text_primary"]).pack(anchor='w')

        dif_entry = tk.Entry(dif_frame, font=('Segoe UI', 11),
                            bg=self.cores["bg_input"], fg=self.cores["text_primary"],
                            relief='flat', bd=5, insertbackground=self.cores["text_primary"])
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
        """OTIMIZADO: Mostrar dicas da pergunta"""
        dicas = pergunta_data.get("dicas", [])
        if dicas:
            dicas_frame = tk.Frame(parent, bg=self.cores["bg_secondary"])
            dicas_frame.pack(fill='x', pady=(5, 0))

            tk.Label(dicas_frame, text="💡 Dicas:",
                    font=('Segoe UI', 10, 'bold'),
                    bg=self.cores["bg_secondary"], fg=self.cores["accent_yellow"]).pack(anchor='w')

            for i, dica in enumerate(dicas, 1):
                if dica.strip():  # Só mostra dicas não vazias
                    tk.Label(dicas_frame, text=f"   {i}. {dica}",
                            font=('Segoe UI', 9),
                            bg=self.cores["bg_secondary"], fg=self.cores["accent_yellow"]).pack(anchor='w')

    def editar_pergunta_por_indice(self, index):
        try:
            pergunta_atual = self.perguntas[index]
            dialog = PerguntaDialogModerno(self.root, pergunta_editada=pergunta_atual)
            if dialog.pergunta and dialog.resposta:
                self.perguntas[index] = {
                    "pergunta": dialog.pergunta,
                    "resposta": dialog.resposta,
                    "dica": dialog.dica,
                    "dicas": getattr(dialog, 'dicas', [dialog.dica] if dialog.dica else []),
                    "dificuldade": getattr(dialog, 'dificuldade', 'medio'),
                    "pontos": getattr(dialog, 'pontos', 20),
                    "tentativas_custom": dialog.tentativas_pergunta,
                    "dicas_custom": dialog.dicas_ativadas_pergunta
                }
                self.atualizar_lista_perguntas()
                self.mostrar_popup("✅ Sucesso", "Pergunta editada com sucesso!", "success")
        except:
            self.mostrar_popup("⚠️ Erro", "Pergunta não encontrada!", "error")

    def remover_pergunta_por_indice(self, index):
        try:
            resultado = self.mostrar_popup_questao("🗑️ Remover Pergunta", f"Deseja realmente remover a Pergunta {index + 1}?")
            if resultado:
                del self.perguntas[index]
                self.atualizar_lista_perguntas()
                self.mostrar_popup("✅ Sucesso", "Pergunta removida com sucesso!", "success")
        except:
            self.mostrar_popup("⚠️ Erro", "Pergunta não encontrada!", "error")

    def adicionar_pergunta(self):
        try:
            dialog = PerguntaDialogModerno(self.root)
            if dialog.pergunta and dialog.resposta:
                self.perguntas.append({
                    "pergunta": dialog.pergunta,
                    "resposta": dialog.resposta,
                    "dica": dialog.dica,
                    "dicas": getattr(dialog, 'dicas', [dialog.dica] if dialog.dica else []),
                    "dificuldade": getattr(dialog, 'dificuldade', 'medio'),
                    "pontos": getattr(dialog, 'pontos', 20),
                    "tentativas_custom": dialog.tentativas_pergunta,
                    "dicas_custom": dialog.dicas_ativadas_pergunta
                })
                self.atualizar_lista_perguntas()
        except:
            pass

    def preparar_perguntas_jogo(self):
        self.perguntas_jogo = self.perguntas.copy()
        if self.configuracoes["ordem_aleatoria"]:
            random.shuffle(self.perguntas_jogo)

    def iniciar_jogo(self):
        if not self.perguntas:
            self.mostrar_popup("⚠️ Atenção", "Adicione pelo menos uma pergunta para começar!", "warning")
            return
        self.preparar_perguntas_jogo()
        self.respostas_usuario = []
        self.pergunta_atual = 0
        self.mostrar_pergunta()

    def mostrar_pergunta(self):
        if self.pergunta_atual >= len(self.perguntas_jogo):
            self.mostrar_resultado_final()
            return

        self.limpar_tela()
        pergunta_config = self.perguntas_jogo[self.pergunta_atual]
        self.tentativas_restantes = pergunta_config.get("tentativas_custom") or self.configuracoes["num_tentativas"]

        main_frame = tk.Frame(self.root, bg=self.cores["bg_primary"])
        main_frame.pack(expand=True, fill='both', padx=25, pady=25)

        header_frame = tk.Frame(main_frame, bg=self.cores["bg_secondary"], relief='solid', bd=2)
        header_frame.pack(fill='x', pady=12)

        tk.Label(header_frame, text=f"🎲 PERGUNTA {self.pergunta_atual + 1} DE {len(self.perguntas_jogo)}", 
                font=('Segoe UI', 22, 'bold'), bg=self.cores["bg_secondary"], fg=self.cores["accent_red"]).pack(pady=18)

        status_frame = tk.Frame(header_frame, bg=self.cores["bg_secondary"])
        status_frame.pack(pady=12)
        tk.Label(status_frame, text=f"🎯 Tentativas: {self.tentativas_restantes}", 
                font=('Segoe UI', 16), bg=self.cores["bg_secondary"], fg=self.cores["accent_orange"]).pack(side='left', padx=25)
        tk.Label(status_frame, text=f"🎲 Sorte: {random.randint(1, 6)}", 
                font=('Segoe UI', 16), bg=self.cores["bg_secondary"], fg=self.cores["accent_green"]).pack(side='right', padx=25)

        pergunta_frame = tk.Frame(main_frame, bg=self.cores["bg_accent"], relief='solid', bd=2)
        pergunta_frame.pack(fill='x', pady=35, padx=25)
        tk.Label(pergunta_frame, text=self.perguntas_jogo[self.pergunta_atual]["pergunta"], font=('Segoe UI', 18), 
                bg=self.cores["bg_accent"], fg=self.cores["text_primary"], wraplength=850, justify='center').pack(pady=35, padx=25)

        resposta_frame = tk.Frame(main_frame, bg=self.cores["bg_primary"])
        resposta_frame.pack(pady=35)
        tk.Label(resposta_frame, text="💭 Sua Resposta:", font=('Segoe UI', 16, 'bold'), 
                bg=self.cores["bg_primary"], fg=self.cores["text_primary"]).pack(pady=12)

        self.entrada_resposta = tk.Entry(resposta_frame, font=('Segoe UI', 18), width=55, relief='flat', bd=8)
        self.entrada_resposta.pack(pady=18)
        self.entrada_resposta.bind('<Return>', lambda e: self.verificar_resposta())
        self.entrada_resposta.focus()

        botoes_acao = tk.Frame(resposta_frame, bg=self.cores["bg_primary"])
        botoes_acao.pack(pady=25)

        mostrar_dicas = self.configuracoes["dicas_ativadas"]
        if pergunta_config.get("dicas_custom") is not None:
            mostrar_dicas = pergunta_config["dicas_custom"]

        dicas = pergunta_config.get("dicas", [])
        if not dicas and pergunta_config.get("dica"):
            dicas = [pergunta_config["dica"]]

        if mostrar_dicas and dicas:
            self.criar_botao_moderno(botoes_acao, "💡 SOLICITAR DICA", self.mostrar_dica_aleatoria, self.cores["accent_yellow"]).pack(side='left', padx=10)

        self.criar_botao_moderno(botoes_acao, "✅ CONFIRMAR RESPOSTA", self.verificar_resposta, self.cores["accent_green"]).pack(side='left', padx=10)

    def mostrar_dica_aleatoria(self):
        try:
            pergunta_config = self.perguntas_jogo[self.pergunta_atual]
            dicas = pergunta_config.get("dicas", [])
            if not dicas and pergunta_config.get("dica"):
                dicas = [pergunta_config["dica"]]

            if dicas:
                dica_selecionada = random.choice(dicas)
                self.mostrar_popup("💡 Dica", f"Aqui está uma dica para você:\n\n{dica_selecionada}", "info")
            else:
                self.mostrar_popup("⚠️ Sem Dicas", "Não há dicas disponíveis para esta pergunta.", "warning")
        except Exception as e:
            self.mostrar_popup("⚠️ Erro", f"Erro ao mostrar dica: {str(e)}", "error")

    def verificar_resposta(self):
        try:
            resposta_usuario = self.entrada_resposta.get().strip()
            resposta_correta = self.perguntas_jogo[self.pergunta_atual]["resposta"]

            if resposta_usuario.lower() == resposta_correta.lower():
                self.processar_resposta_correta(resposta_usuario, resposta_correta)
            else:
                self.processar_resposta_incorreta(resposta_usuario, resposta_correta)
        except Exception as e:
            self.mostrar_popup("⚠️ Erro", f"Erro ao verificar resposta: {str(e)}", "error")

    def processar_resposta_correta(self, resposta_usuario, resposta_correta):
        """OTIMIZADO: Processar resposta correta"""
        self.respostas_usuario.append({
            "pergunta": self.perguntas_jogo[self.pergunta_atual]["pergunta"],
            "resposta_correta": resposta_correta,
            "resposta_usuario": resposta_usuario,
            "acertou": True,
            "tentativas_usadas": self.configuracoes["num_tentativas"] - self.tentativas_restantes + 1
        })
        self.mostrar_popup("🎉 Correto!", "Excelente! Você acertou!\nAvançando para próxima pergunta...", "success")
        self.pergunta_atual += 1
        self.mostrar_pergunta()

    def processar_resposta_incorreta(self, resposta_usuario, resposta_correta):
        """OTIMIZADO: Processar resposta incorreta"""
        self.tentativas_restantes -= 1
        if self.tentativas_restantes > 0:
            self.mostrar_dica_tentativa()
            self.entrada_resposta.delete(0, tk.END)
            self.entrada_resposta.focus()
        else:
            self.processar_fim_tentativas(resposta_usuario, resposta_correta)

    def mostrar_dica_tentativa(self):
        """OTIMIZADO: Mostrar dica baseada na tentativa"""
        dica_texto = ""
        pergunta_config = self.perguntas_jogo[self.pergunta_atual]
        mostrar_dicas = self.configuracoes["dicas_ativadas"]

        if pergunta_config.get("dicas_custom") is not None:
            mostrar_dicas = pergunta_config["dicas_custom"]

        if mostrar_dicas:
            dicas = pergunta_config.get("dicas", [])
            if not dicas and pergunta_config.get("dica"):
                dicas = [pergunta_config["dica"]]

            if dicas:
                tentativas_usadas = self.configuracoes["num_tentativas"] - self.tentativas_restantes
                if tentativas_usadas > 0 and tentativas_usadas <= len(dicas):
                    dica_atual = dicas[tentativas_usadas - 1]
                    dica_texto = f"\n\n💡 Dica {tentativas_usadas}: {dica_atual}"

        mensagem = f"Resposta incorreta!\nTentativas restantes: {self.tentativas_restantes}{dica_texto}"
        self.mostrar_popup("❌ Incorreto", mensagem, "warning")

    def processar_fim_tentativas(self, resposta_usuario, resposta_correta):
        """OTIMIZADO: Processar fim de tentativas"""
        self.respostas_usuario.append({
            "pergunta": self.perguntas_jogo[self.pergunta_atual]["pergunta"],
            "resposta_correta": resposta_correta,
            "resposta_usuario": resposta_usuario,
            "acertou": False,
            "tentativas_usadas": self.configuracoes["num_tentativas"]
        })
        mensagem = f"Tentativas esgotadas!\nA resposta correta era: {resposta_correta}"
        self.mostrar_popup("😞 Fim das Tentativas", mensagem, "error")
        self.pergunta_atual += 1
        self.mostrar_pergunta()

    def mostrar_resultado_final(self):
        self.limpar_tela()

        main_frame = tk.Frame(self.root, bg=self.cores["bg_primary"])
        main_frame.pack(expand=True, fill='both', padx=25, pady=25)

        titulo = tk.Label(main_frame, text="🏆 AVENTURA CONCLUÍDA", 
                         font=('Segoe UI', 32, 'bold'),
                         bg=self.cores["bg_primary"], fg=self.cores["accent_purple"])
        titulo.pack(pady=35)

        # Estatísticas
        self.mostrar_estatisticas_finais(main_frame)

        # Lista de resultados com scroll
        self.criar_lista_resultados(main_frame)

        # Botões de navegação
        self.criar_botoes_navegacao_final(main_frame)

    def mostrar_estatisticas_finais(self, parent):
        """OTIMIZADO: Mostrar estatísticas finais"""
        acertos = sum(1 for r in self.respostas_usuario if r["acertou"])
        total = len(self.respostas_usuario)
        porcentagem = (acertos / total) * 100 if total > 0 else 0

        stats_frame = tk.Frame(parent, bg=self.cores["bg_secondary"], relief='solid', bd=2)
        stats_frame.pack(fill='x', pady=25)

        stats_text = f"📊 PONTUAÇÃO FINAL: {acertos}/{total} ({porcentagem:.1f}%)"
        tk.Label(stats_frame, text=stats_text, 
                font=('Segoe UI', 20, 'bold'), bg=self.cores["bg_secondary"], fg=self.cores["accent_green"]).pack(pady=25)

    def criar_lista_resultados(self, parent):
        """OTIMIZADO: Criar lista de resultados"""
        resultado_frame = tk.Frame(parent, bg=self.cores["bg_accent"])
        resultado_frame.pack(fill='both', expand=True, pady=12)

        try:
            canvas = tk.Canvas(resultado_frame, bg=self.cores["bg_accent"])
            scrollbar = ttk.Scrollbar(resultado_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.cores["bg_accent"])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Configurar scroll com mouse wheel para resultados
            def on_result_mousewheel(event):
                try:
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                except:
                    pass

            def on_result_mousewheel_linux_up(event):
                try:
                    canvas.yview_scroll(-1, "units")
                except:
                    pass

            def on_result_mousewheel_linux_down(event):
                try:
                    canvas.yview_scroll(1, "units")
                except:
                    pass

            # Bind do scroll do mouse
            canvas.bind("<MouseWheel>", on_result_mousewheel)
            canvas.bind("<Button-4>", on_result_mousewheel_linux_up)
            canvas.bind("<Button-5>", on_result_mousewheel_linux_down)

            # Bind para widgets filhos
            def bind_result_scroll_to_children(widget):
                try:
                    widget.bind("<MouseWheel>", on_result_mousewheel)
                    widget.bind("<Button-4>", on_result_mousewheel_linux_up)
                    widget.bind("<Button-5>", on_result_mousewheel_linux_down)
                    for child in widget.winfo_children():
                        bind_result_scroll_to_children(child)
                except:
                    pass

            for i, resposta in enumerate(self.respostas_usuario):
                self.criar_item_resultado(scrollable_frame, i, resposta)

            # Aplicar scroll aos itens criados
            bind_result_scroll_to_children(scrollable_frame)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        except:
            # Fallback simples se o scroll não funcionar
            tk.Label(resultado_frame, text="Resultados exibidos com sucesso!", 
                    font=('Segoe UI', 14), bg=self.cores["bg_accent"], fg=self.cores["text_primary"]).pack(pady=20)

    def criar_item_resultado(self, parent, index, resposta):
        """OTIMIZADO: Criar item de resultado"""
        item_frame = tk.Frame(parent, bg=self.cores["bg_secondary"], relief='solid', bd=1)
        item_frame.pack(fill='x', pady=8, padx=12)

        status = "✅ CORRETO" if resposta["acertou"] else "❌ INCORRETO"
        cor = self.cores["accent_green"] if resposta["acertou"] else self.cores["accent_red"]

        tk.Label(item_frame, text=f"{index+1}. {status}", 
                font=('Segoe UI', 16, 'bold'), bg=self.cores["bg_secondary"], fg=cor).pack(anchor='w', padx=18, pady=10)

        tk.Label(item_frame, text=f"Pergunta: {resposta['pergunta']}", 
                font=('Segoe UI', 12), bg=self.cores["bg_secondary"], fg=self.cores["text_primary"], 
                wraplength=750).pack(anchor='w', padx=30)

        tk.Label(item_frame, text=f"Resposta correta: {resposta['resposta_correta']}", 
                font=('Segoe UI', 12), bg=self.cores["bg_secondary"], fg=self.cores["accent_green"]).pack(anchor='w', padx=30)

        tk.Label(item_frame, text=f"Sua resposta: {resposta['resposta_usuario']}", 
                font=('Segoe UI', 12), bg=self.cores["bg_secondary"], fg=self.cores["text_secondary"]).pack(anchor='w', padx=30)

        tk.Label(item_frame, text=f"Tentativas usadas: {resposta['tentativas_usadas']}", 
                font=('Segoe UI', 12), bg=self.cores["bg_secondary"], fg=self.cores["accent_orange"]).pack(anchor='w', padx=30, pady=(0,10))

    def criar_botoes_navegacao_final(self, parent):
        """OTIMIZADO: Criar botões de navegação final"""
        navegacao_frame = tk.Frame(parent, bg=self.cores["bg_primary"])
        navegacao_frame.pack(side='bottom', fill='x', pady=25)

        tk.Label(navegacao_frame, text="Escolha sua próxima ação:", 
                font=('Segoe UI', 16), bg=self.cores["bg_primary"], fg=self.cores["text_secondary"]).pack(pady=12)

        botoes_navegacao_frame = tk.Frame(navegacao_frame, bg=self.cores["bg_primary"])
        botoes_navegacao_frame.pack(pady=15)

        btn_recomecar = tk.Button(botoes_navegacao_frame, text="🔄 RECOMEÇAR AVENTURA", 
                                 command=self.recomecar_jogo,
                                 font=('Segoe UI', 20, 'bold'), 
                                 bg=self.cores["accent_green"], fg="white", relief='flat',
                                 padx=60, pady=35, cursor='hand2', width=20, height=2)
        btn_recomecar.pack(side='left', padx=30)

        btn_lobby = tk.Button(botoes_navegacao_frame, text="🏠 RETORNAR AO LOBBY", 
                             command=self.criar_menu_principal,
                             font=('Segoe UI', 20, 'bold'), 
                             bg=self.cores["accent_blue"], fg="white", relief='flat',
                             padx=60, pady=35, cursor='hand2', width=20, height=2)
        btn_lobby.pack(side='left', padx=30)

    def recomecar_jogo(self):
        """Reinicia o jogo com as mesmas perguntas"""
        if not self.perguntas:
            self.mostrar_popup("⚠️ Atenção", "Não há perguntas para recomeçar!", "warning")
            self.criar_menu_principal()
            return

        resultado = self.mostrar_popup_questao("🔄 Recomeçar Aventura", 
                                              "Deseja recomeçar a aventura com as mesmas perguntas?")
        if resultado:
            # OTIMIZADO: Usar método de reset
            self.respostas_usuario = []
            self.pergunta_atual = 0
            self.tentativas_restantes = 0

            # NOVO: Preparar perguntas novamente (pode embaralhar diferente)
            self.preparar_perguntas_jogo()
            self.mostrar_pergunta()

    def sair_jogo(self):
        resultado = self.mostrar_popup_questao("🚪 Sair do Jogo", "Tem certeza que deseja sair da aventura?")
        if resultado:
            self.root.quit()

    def executar(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Erro ao executar o jogo: {e}")

class PerguntaDialogModerno:
    def __init__(self, parent, pergunta_editada=None):
        self.resultado_data = {'pergunta': None, 'resposta': None, 'dica': None, 'dificuldade': None, 
                              'pontos': None, 'tentativas_pergunta': None, 'dicas_ativadas_pergunta': None}
        self.parent = parent
        self.editando = pergunta_editada is not None
        self.dados_edicao = pergunta_editada

        try:
            self.criar_dialog()
            self.dicas_entries = []
            self.criar_interface()
            self.dialog.wait_window()
        except:
            self.dialog_simples(parent)

    @property
    def pergunta(self):
        return self.resultado_data['pergunta']

    @property
    def resposta(self):
        return self.resultado_data['resposta']

    @property
    def dica(self):
        return self.resultado_data['dica']

    @property
    def dificuldade(self):
        return self.resultado_data['dificuldade']

    @property
    def pontos(self):
        return self.resultado_data['pontos']

    @property
    def tentativas_pergunta(self):
        return self.resultado_data['tentativas_pergunta']

    @property
    def dicas_ativadas_pergunta(self):
        return self.resultado_data['dicas_ativadas_pergunta']

    def criar_dialog(self):
        self.dialog = tk.Toplevel(self.parent)
        titulo_dialog = "Editar Pergunta" if self.editando else "Nova Pergunta"
        self.dialog.title(titulo_dialog)
        self.dialog.geometry("750x750")
        self.dialog.configure(bg="#2c3e50")
        self.dialog.resizable(True, True)
        self.dialog.minsize(700, 700)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        try:
            self.parent.update_idletasks()
            x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 375
            y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 375
            self.dialog.geometry(f"750x750+{x}+{y}")
        except:
            self.dialog.geometry("750x750+200+50")

    def dialog_simples(self, parent):
        try:
            pergunta = simpledialog.askstring("Pergunta", "Digite a pergunta:")
            if pergunta:
                resposta = simpledialog.askstring("Resposta", "Digite a resposta correta:")
                if resposta:
                    dica = simpledialog.askstring("Dica", "Digite uma dica (opcional):") or ""
                    self.resultado_data.update({'pergunta': pergunta, 'resposta': resposta, 'dica': dica})
        except Exception as e:
            print(f"Erro no dialog simples: {e}")

    def criar_interface(self):
        main_frame = tk.Frame(self.dialog, bg="#34495e", relief='solid', bd=2)
        main_frame.pack(fill='both', expand=True, padx=3, pady=3)

        title_frame = tk.Frame(main_frame, bg="#2c3e50", height=55)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        titulo_barra = "✏️ EDITAR PERGUNTA" if self.editando else "📝 CRIAR NOVA PERGUNTA"
        tk.Label(title_frame, text=titulo_barra, font=('Segoe UI', 18, 'bold'), 
                bg="#2c3e50", fg="#ecf0f1").pack(side='left', padx=25, pady=18)

        tk.Button(title_frame, text="✕", font=('Segoe UI', 13, 'bold'),
                 bg="#e74c3c", fg="white", relief='flat', width=3, height=1,
                 command=self.cancelar).pack(side='right', padx=18, pady=15)

        canvas = tk.Canvas(main_frame, bg="#34495e", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg="#34495e")

        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_dialog_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass

        def on_dialog_mousewheel_linux_up(event):
            try:
                canvas.yview_scroll(-1, "units")
            except:
                pass

        def on_dialog_mousewheel_linux_down(event):
            try:
                canvas.yview_scroll(1, "units")
            except:
                pass

        # Bind do scroll do mouse
        canvas.bind("<MouseWheel>", on_dialog_mousewheel)
        canvas.bind("<Button-4>", on_dialog_mousewheel_linux_up)
        canvas.bind("<Button-5>", on_dialog_mousewheel_linux_down)

        # Bind para widgets filhos do content_frame
        def bind_dialog_scroll_to_children(widget):
            try:
                widget.bind("<MouseWheel>", on_dialog_mousewheel)
                widget.bind("<Button-4>", on_dialog_mousewheel_linux_up)
                widget.bind("<Button-5>", on_dialog_mousewheel_linux_down)
                for child in widget.winfo_children():
                    bind_dialog_scroll_to_children(child)
            except:
                pass

        content_frame.bind("<Configure>", 
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), 
                      bind_dialog_scroll_to_children(content_frame)])

        canvas.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        scrollbar.pack(side="right", fill="y", pady=30)

        self.criar_campos_formulario(content_frame)

    def criar_campos_formulario(self, parent):
        # Pergunta
        tk.Label(parent, text="🤔 Pergunta:", font=('Segoe UI', 16, 'bold'), 
                bg="#34495e", fg="#ecf0f1").pack(anchor='w', pady=(12,8))
        self.entry_pergunta = tk.Text(parent, height=4, font=('Segoe UI', 13),
                                     bg="#ecf0f1", fg="#7f8c8d", relief='flat', bd=8,
                                     insertbackground="#2c3e50", width=60)
        self.entry_pergunta.pack(fill='x', pady=(0,18))
        self.configurar_placeholder_text_widget(self.entry_pergunta, "Digite a pergunta...")

        # Resposta
        tk.Label(parent, text="✅ Resposta Correta:", font=('Segoe UI', 16, 'bold'), 
                bg="#34495e", fg="#ecf0f1").pack(anchor='w', pady=(12,8))
        self.entry_resposta = tk.Entry(parent, font=('Segoe UI', 13), width=60,
                                      bg="#ecf0f1", fg="#7f8c8d", relief='flat', bd=8,
                                      insertbackground="#2c3e50")
        self.entry_resposta.pack(fill='x', pady=(0,18))
        self.configurar_placeholder_entry_widget(self.entry_resposta, "Digite a resposta correta...")

        # Dificuldade
        tk.Label(parent, text="⭐ Dificuldade:", font=('Segoe UI', 16, 'bold'), 
                bg="#34495e", fg="#ecf0f1").pack(pady=(12,8))

        self.dificuldade_var = tk.StringVar(value="medio")
        dificuldade_frame = tk.Frame(parent, bg="#34495e")
        dificuldade_frame.pack(pady=(0,25))

        for texto, valor, pontos, cor in [("Fácil", "facil", 10, "#27ae60"), ("Médio", "medio", 20, "#f39c12"), ("Difícil", "dificil", 30, "#e74c3c")]:
            dif_container = tk.Frame(dificuldade_frame, bg=cor, relief='solid', bd=2)
            dif_container.pack(side='left', padx=15, pady=5)
            tk.Radiobutton(dif_container, text=f"{texto}\n({pontos} pts)", variable=self.dificuldade_var, value=valor, 
                          font=('Segoe UI', 12, 'bold'), bg=cor, fg="white", selectcolor=cor, 
                          activebackground=cor, activeforeground="white", padx=15, pady=10,
                          indicatoron=False, width=8, height=2).pack()

        # Dicas
        tk.Label(parent, text="💡 Dicas (opcional):", font=('Segoe UI', 16, 'bold'), 
                bg="#34495e", fg="#ecf0f1").pack(anchor='w', pady=(12,8))

        self.dicas_frame = tk.Frame(parent, bg="#34495e")
        self.dicas_frame.pack(fill='x', pady=(0,15))
        self.dicas_entries = []
        self.adicionar_campo_dica()

        tk.Button(parent, text="+ Adicionar Dica", command=self.adicionar_campo_dica,
                 bg="#f39c12", fg="white", font=('Segoe UI', 12, 'bold'), relief='flat', 
                 padx=20, pady=8, cursor='hand2').pack(pady=(0,15))

        # Botões
        botoes_frame = tk.Frame(parent, bg="#34495e")
        botoes_frame.pack(pady=30)
        tk.Button(botoes_frame, text="💾 SALVAR PERGUNTA", command=self.salvar, 
                 bg="#27ae60", fg="white", font=('Segoe UI', 14, 'bold'), relief='flat', 
                 padx=30, pady=15, cursor='hand2').pack(side='left', padx=15)
        tk.Button(botoes_frame, text="❌ CANCELAR", command=self.cancelar, 
                 bg="#e74c3c", fg="white", font=('Segoe UI', 14, 'bold'), relief='flat', 
                 padx=30, pady=15, cursor='hand2').pack(side='left', padx=15)

        if self.editando and self.dados_edicao:
            self.carregar_dados_edicao()

        try:
            self.entry_pergunta.focus()
        except:
            pass

    def configurar_placeholder_text_widget(self, widget, placeholder):
        """OTIMIZADO: Placeholder para Text widget"""
        widget.insert("1.0", placeholder)
        
        def on_focus_in(event):
            content = widget.get("1.0", tk.END).strip()
            if content == placeholder:
                widget.delete("1.0", tk.END)
                widget.config(fg="#2c3e50")

        def on_focus_out(event):
            content = widget.get("1.0", tk.END).strip()
            if not content:
                widget.insert("1.0", placeholder)
                widget.config(fg="#7f8c8d")

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    def configurar_placeholder_entry_widget(self, widget, placeholder):
        """OTIMIZADO: Placeholder para Entry widget"""
        widget.insert(0, placeholder)
        
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg="#2c3e50")

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#7f8c8d")

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    def adicionar_campo_dica(self):
        dica_container = tk.Frame(self.dicas_frame, bg="#34495e")
        dica_container.pack(fill='x', pady=5)

        entry_dica = tk.Entry(dica_container, font=('Segoe UI', 13), 
                             bg="#ecf0f1", fg="#2c3e50", relief='flat', bd=8,
                             insertbackground="#2c3e50")
        entry_dica.pack(side='left', fill='x', expand=True, padx=(0, 10))

        placeholder_text = f"Digite a dica {len(self.dicas_entries) + 1} (opcional)..."
        entry_dica.config(fg="#7f8c8d")
        entry_dica.insert(0, placeholder_text)
        entry_dica.placeholder_active = True
        entry_dica.placeholder_text = placeholder_text

        tk.Button(dica_container, text="❌", bg="#e74c3c", fg="white", 
                 font=('Segoe UI', 10, 'bold'), relief='flat', width=3, height=1, cursor='hand2',
                 command=lambda: self.remover_campo_dica(dica_container, entry_dica)).pack(side='right')

        def on_dica_focus_in(event):
            if entry_dica.placeholder_active:
                entry_dica.delete(0, tk.END)
                entry_dica.config(fg="#2c3e50")
                entry_dica.placeholder_active = False

        def on_dica_focus_out(event):
            if not entry_dica.get().strip():
                entry_dica.delete(0, tk.END)
                entry_dica.insert(0, entry_dica.placeholder_text)
                entry_dica.config(fg="#7f8c8d")
                entry_dica.placeholder_active = True

        def on_key_press(event):
            if entry_dica.placeholder_active:
                entry_dica.delete(0, tk.END)
                entry_dica.config(fg="#2c3e50")
                entry_dica.placeholder_active = False

        entry_dica.bind("<FocusIn>", on_dica_focus_in)
        entry_dica.bind("<FocusOut>", on_dica_focus_out)
        entry_dica.bind("<KeyPress>", on_key_press)

        self.dicas_entries.append(entry_dica)
        entry_dica.focus()

    def remover_campo_dica(self, container, entry):
        if len(self.dicas_entries) > 1:
            self.dicas_entries.remove(entry)
            container.destroy()
            self.atualizar_placeholders_dicas()

    def atualizar_placeholders_dicas(self):
        for i, entry in enumerate(self.dicas_entries, 1):
            if entry.placeholder_active:
                entry.delete(0, tk.END)
                novo_placeholder = f"Digite a dica {i} (opcional)..."
                entry.insert(0, novo_placeholder)
                entry.placeholder_text = novo_placeholder

    def salvar(self):
        try:
            pergunta = self.entry_pergunta.get("1.0", tk.END).strip()
            resposta = self.entry_resposta.get().strip()

            if not pergunta or pergunta == "Digite a pergunta...":
                try:
                    PopupModerno(self.dialog, "⚠️ Campo Obrigatório", "Por favor, digite uma pergunta!", "warning")
                except:
                    messagebox.showwarning("Campo Obrigatório", "Por favor, digite uma pergunta!")
                self.entry_pergunta.focus()
                return

            if not resposta or resposta == "Digite a resposta correta...":
                try:
                    PopupModerno(self.dialog, "⚠️ Campo Obrigatório", "Por favor, digite a resposta correta!", "warning")
                except:
                    messagebox.showwarning("Campo Obrigatório", "Por favor, digite a resposta correta!")
                self.entry_resposta.focus()
                return

            dicas_lista = []
            for entry in self.dicas_entries:
                if not entry.placeholder_active:
                    dica_texto = entry.get().strip()
                    if dica_texto:
                        dicas_lista.append(dica_texto)

            dificuldade_selecionada = self.dificuldade_var.get()
            pontos_dificuldade = {"facil": 10, "medio": 20, "dificil": 30}
            pontos = pontos_dificuldade.get(dificuldade_selecionada, 20)

            self.resultado_data.update({
                'pergunta': pergunta,
                'resposta': resposta,
                'dica': dicas_lista[0] if dicas_lista else "",
                'dificuldade': dificuldade_selecionada,
                'pontos': pontos
            })

            self.dicas = dicas_lista

            try:
                PopupModerno(self.dialog, "✅ Pergunta Salva", "Pergunta adicionada com sucesso!", "success")
            except:
                print("Pergunta salva com sucesso!")

            self.dialog.destroy()

        except Exception as e:
            try:
                PopupModerno(self.dialog, "❌ Erro", f"Erro ao salvar pergunta: {str(e)}", "error")
            except:
                messagebox.showerror("Erro", f"Erro ao salvar pergunta: {str(e)}")

    def carregar_dados_edicao(self):
        try:
            pergunta_texto = self.dados_edicao.get("pergunta", "")
            if pergunta_texto:
                self.entry_pergunta.delete("1.0", tk.END)
                self.entry_pergunta.insert("1.0", pergunta_texto)
                self.entry_pergunta.config(fg="#2c3e50")

            resposta_texto = self.dados_edicao.get("resposta", "")
            if resposta_texto:
                self.entry_resposta.delete(0, tk.END)
                self.entry_resposta.insert(0, resposta_texto)
                self.entry_resposta.config(fg="#2c3e50")

            dificuldade = self.dados_edicao.get("dificuldade", "medio")
            self.dificuldade_var.set(dificuldade)

            dicas_existentes = self.dados_edicao.get("dicas", [])
            if not dicas_existentes and self.dados_edicao.get("dica"):
                dicas_existentes = [self.dados_edicao["dica"]]

            for entry in self.dicas_entries:
                entry.master.destroy()
            self.dicas_entries.clear()

            if dicas_existentes:
                for dica_texto in dicas_existentes:
                    self.adicionar_campo_dica()
                    entry = self.dicas_entries[-1]
                    entry.delete(0, tk.END)
                    entry.insert(0, dica_texto)
                    entry.config(fg="#2c3e50")
                    entry.placeholder_active = False
            else:
                self.adicionar_campo_dica()
        except Exception as e:
            print(f"Erro ao carregar dados para edição: {e}")

    def cancelar(self):
        try:
            self.dialog.destroy()
        except:
            pass

if __name__ == "__main__":
    try:
        jogo = JogoEducativoRPG()
        jogo.executar()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        import tkinter.messagebox as mb
        mb.showerror("Erro", f"Erro ao iniciar o jogo: {e}")