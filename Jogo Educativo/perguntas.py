
"""
Gerenciamento de perguntas do RPG Educativo
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import random
from config import CORES, DIFICULDADES
from utils import PopupModerno, configurar_scroll_mouse, bind_scroll_to_children

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
        self.dialog.configure(bg=CORES["bg_secondary"])
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
        main_frame = tk.Frame(self.dialog, bg=CORES["bg_accent"], relief='solid', bd=2)
        main_frame.pack(fill='both', expand=True, padx=3, pady=3)

        title_frame = tk.Frame(main_frame, bg=CORES["bg_secondary"], height=55)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        titulo_barra = "✏️ EDITAR PERGUNTA" if self.editando else "📝 CRIAR NOVA PERGUNTA"
        tk.Label(title_frame, text=titulo_barra, font=('Segoe UI', 18, 'bold'), 
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(side='left', padx=25, pady=18)

        tk.Button(title_frame, text="✕", font=('Segoe UI', 13, 'bold'),
                 bg=CORES["accent_red"], fg="white", relief='flat', width=3, height=1,
                 command=self.cancelar).pack(side='right', padx=18, pady=15)

        canvas = tk.Canvas(main_frame, bg=CORES["bg_accent"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=CORES["bg_accent"])

        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_functions = configurar_scroll_mouse(canvas)

        content_frame.bind("<Configure>", 
            lambda e: [canvas.configure(scrollregion=canvas.bbox("all")), 
                      bind_scroll_to_children(content_frame, scroll_functions)])

        canvas.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        scrollbar.pack(side="right", fill="y", pady=30)

        self.criar_campos_formulario(content_frame)

    def criar_campos_formulario(self, parent):
        # Pergunta
        tk.Label(parent, text="🤔 Pergunta:", font=('Segoe UI', 16, 'bold'), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(anchor='w', pady=(12,8))
        self.entry_pergunta = tk.Text(parent, height=4, font=('Segoe UI', 13),
                                     bg=CORES["text_primary"], fg="#7f8c8d", relief='flat', bd=8,
                                     insertbackground=CORES["bg_secondary"], width=60)
        self.entry_pergunta.pack(fill='x', pady=(0,18))
        self.configurar_placeholder_text_widget(self.entry_pergunta, "Digite a pergunta...")

        # Resposta
        tk.Label(parent, text="✅ Resposta Correta:", font=('Segoe UI', 16, 'bold'), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(anchor='w', pady=(12,8))
        self.entry_resposta = tk.Entry(parent, font=('Segoe UI', 13), width=60,
                                      bg=CORES["text_primary"], fg="#7f8c8d", relief='flat', bd=8,
                                      insertbackground=CORES["bg_secondary"])
        self.entry_resposta.pack(fill='x', pady=(0,18))
        self.configurar_placeholder_entry_widget(self.entry_resposta, "Digite a resposta correta...")

        # Dificuldade
        tk.Label(parent, text="⭐ Dificuldade:", font=('Segoe UI', 16, 'bold'), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(pady=(12,8))

        self.dificuldade_var = tk.StringVar(value="medio")
        dificuldade_frame = tk.Frame(parent, bg=CORES["bg_accent"])
        dificuldade_frame.pack(pady=(0,25))

        for dif_key, dif_data in DIFICULDADES.items():
            texto = dif_key.capitalize()
            pontos = dif_data["pontos"]
            cor = dif_data["cor"]
            
            dif_container = tk.Frame(dificuldade_frame, bg=cor, relief='solid', bd=2)
            dif_container.pack(side='left', padx=15, pady=5)
            tk.Radiobutton(dif_container, text=f"{texto}\n({pontos} pts)", variable=self.dificuldade_var, value=dif_key, 
                          font=('Segoe UI', 12, 'bold'), bg=cor, fg="white", selectcolor=cor, 
                          activebackground=cor, activeforeground="white", padx=15, pady=10,
                          indicatoron=False, width=8, height=2).pack()

        # Dicas
        tk.Label(parent, text="💡 Dicas (opcional):", font=('Segoe UI', 16, 'bold'), 
                bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(anchor='w', pady=(12,8))

        self.dicas_frame = tk.Frame(parent, bg=CORES["bg_accent"])
        self.dicas_frame.pack(fill='x', pady=(0,15))
        self.dicas_entries = []
        self.adicionar_campo_dica()

        tk.Button(parent, text="+ Adicionar Dica", command=self.adicionar_campo_dica,
                 bg=CORES["accent_orange"], fg="white", font=('Segoe UI', 12, 'bold'), relief='flat', 
                 padx=20, pady=8, cursor='hand2').pack(pady=(0,15))

        # Botões
        botoes_frame = tk.Frame(parent, bg=CORES["bg_accent"])
        botoes_frame.pack(pady=30)
        tk.Button(botoes_frame, text="💾 SALVAR PERGUNTA", command=self.salvar, 
                 bg=CORES["accent_green"], fg="white", font=('Segoe UI', 14, 'bold'), relief='flat', 
                 padx=30, pady=15, cursor='hand2').pack(side='left', padx=15)
        tk.Button(botoes_frame, text="❌ CANCELAR", command=self.cancelar, 
                 bg=CORES["accent_red"], fg="white", font=('Segoe UI', 14, 'bold'), relief='flat', 
                 padx=30, pady=15, cursor='hand2').pack(side='left', padx=15)

        if self.editando and self.dados_edicao:
            self.carregar_dados_edicao()

        try:
            self.entry_pergunta.focus()
        except:
            pass

    def configurar_placeholder_text_widget(self, widget, placeholder):
        """Configurar placeholder para Text widget"""
        widget.insert("1.0", placeholder)
        
        def on_focus_in(event):
            content = widget.get("1.0", tk.END).strip()
            if content == placeholder:
                widget.delete("1.0", tk.END)
                widget.config(fg=CORES["bg_secondary"])

        def on_focus_out(event):
            content = widget.get("1.0", tk.END).strip()
            if not content:
                widget.insert("1.0", placeholder)
                widget.config(fg="#7f8c8d")

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    def configurar_placeholder_entry_widget(self, widget, placeholder):
        """Configurar placeholder para Entry widget"""
        widget.insert(0, placeholder)
        
        def on_focus_in(event):
            if widget.get() == placeholder:
                widget.delete(0, tk.END)
                widget.config(fg=CORES["bg_secondary"])

        def on_focus_out(event):
            if not widget.get():
                widget.insert(0, placeholder)
                widget.config(fg="#7f8c8d")

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)

    def adicionar_campo_dica(self):
        dica_container = tk.Frame(self.dicas_frame, bg=CORES["bg_accent"])
        dica_container.pack(fill='x', pady=5)

        entry_dica = tk.Entry(dica_container, font=('Segoe UI', 13), 
                             bg=CORES["text_primary"], fg=CORES["bg_secondary"], relief='flat', bd=8,
                             insertbackground=CORES["bg_secondary"])
        entry_dica.pack(side='left', fill='x', expand=True, padx=(0, 10))

        placeholder_text = f"Digite a dica {len(self.dicas_entries) + 1} (opcional)..."
        entry_dica.config(fg="#7f8c8d")
        entry_dica.insert(0, placeholder_text)
        entry_dica.placeholder_active = True
        entry_dica.placeholder_text = placeholder_text

        tk.Button(dica_container, text="❌", bg=CORES["accent_red"], fg="white", 
                 font=('Segoe UI', 10, 'bold'), relief='flat', width=3, height=1, cursor='hand2',
                 command=lambda: self.remover_campo_dica(dica_container, entry_dica)).pack(side='right')

        def on_dica_focus_in(event):
            if entry_dica.placeholder_active:
                entry_dica.delete(0, tk.END)
                entry_dica.config(fg=CORES["bg_secondary"])
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
                entry_dica.config(fg=CORES["bg_secondary"])
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
            pontos = DIFICULDADES.get(dificuldade_selecionada, DIFICULDADES["medio"])["pontos"]

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
                self.entry_pergunta.config(fg=CORES["bg_secondary"])

            resposta_texto = self.dados_edicao.get("resposta", "")
            if resposta_texto:
                self.entry_resposta.delete(0, tk.END)
                self.entry_resposta.insert(0, resposta_texto)
                self.entry_resposta.config(fg=CORES["bg_secondary"])

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
                    entry.config(fg=CORES["bg_secondary"])
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

class GerenciadorPerguntas:
    def __init__(self):
        self.perguntas = []
        self.perguntas_jogo = []
        
    def adicionar_pergunta(self, pergunta_data):
        """Adicionar uma nova pergunta"""
        self.perguntas.append(pergunta_data)
        
    def remover_pergunta(self, index):
        """Remover pergunta por índice"""
        if 0 <= index < len(self.perguntas):
            del self.perguntas[index]
            return True
        return False
        
    def editar_pergunta(self, index, pergunta_data):
        """Editar pergunta existente"""
        if 0 <= index < len(self.perguntas):
            self.perguntas[index] = pergunta_data
            return True
        return False
        
    def preparar_perguntas_jogo(self, embaralhar=False):
        """Preparar perguntas para o jogo"""
        self.perguntas_jogo = self.perguntas.copy()
        if embaralhar:
            random.shuffle(self.perguntas_jogo)
            
    def obter_pergunta(self, index):
        """Obter pergunta por índice"""
        if 0 <= index < len(self.perguntas_jogo):
            return self.perguntas_jogo[index]
        return None
        
    def total_perguntas(self):
        """Total de perguntas"""
        return len(self.perguntas)
        
    def total_perguntas_jogo(self):
        """Total de perguntas no jogo atual"""
        return len(self.perguntas_jogo)
        
    def limpar_perguntas(self):
        """Limpar todas as perguntas"""
        self.perguntas.clear()
        self.perguntas_jogo.clear()
