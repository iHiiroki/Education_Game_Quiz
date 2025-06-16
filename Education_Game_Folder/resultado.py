
"""
Tela de resultados do RPG Educativo
"""

import tkinter as tk
from tkinter import ttk
from config import CORES
from utils import configurar_scroll_mouse, bind_scroll_to_children

class TelaResultados:
    def __init__(self, parent, respostas_usuario, callback_recomecar, callback_menu):
        self.parent = parent
        self.respostas_usuario = respostas_usuario
        self.callback_recomecar = callback_recomecar
        self.callback_menu = callback_menu
        
    def criar_tela_resultados(self):
        """Criar interface da tela de resultados"""
        main_frame = tk.Frame(self.parent, bg=CORES["bg_primary"])
        main_frame.pack(expand=True, fill='both', padx=25, pady=25)

        titulo = tk.Label(main_frame, text="🏆 AVENTURA CONCLUÍDA", 
                         font=('Segoe UI', 32, 'bold'),
                         bg=CORES["bg_primary"], fg=CORES["accent_purple"])
        titulo.pack(pady=35)

        # Estatísticas
        self._mostrar_estatisticas_finais(main_frame)

        # Lista de resultados com scroll
        self._criar_lista_resultados(main_frame)

        # Botões de navegação
        self._criar_botoes_navegacao_final(main_frame)

    def _mostrar_estatisticas_finais(self, parent):
        """Mostrar estatísticas finais"""
        acertos = sum(1 for r in self.respostas_usuario if r["acertou"])
        total = len(self.respostas_usuario)
        porcentagem = (acertos / total) * 100 if total > 0 else 0

        stats_frame = tk.Frame(parent, bg=CORES["bg_secondary"], relief='solid', bd=2)
        stats_frame.pack(fill='x', pady=25)

        stats_text = f"📊 PONTUAÇÃO FINAL: {acertos}/{total} ({porcentagem:.1f}%)"
        tk.Label(stats_frame, text=stats_text, 
                font=('Segoe UI', 20, 'bold'), bg=CORES["bg_secondary"], fg=CORES["accent_green"]).pack(pady=25)

    def _criar_lista_resultados(self, parent):
        """Criar lista de resultados"""
        resultado_frame = tk.Frame(parent, bg=CORES["bg_accent"])
        resultado_frame.pack(fill='both', expand=True, pady=12)

        try:
            canvas = tk.Canvas(resultado_frame, bg=CORES["bg_accent"])
            scrollbar = ttk.Scrollbar(resultado_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=CORES["bg_accent"])

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            scroll_functions = configurar_scroll_mouse(canvas)

            for i, resposta in enumerate(self.respostas_usuario):
                self._criar_item_resultado(scrollable_frame, i, resposta)

            # Aplicar scroll aos itens criados
            bind_scroll_to_children(scrollable_frame, scroll_functions)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        except:
            # Fallback simples se o scroll não funcionar
            tk.Label(resultado_frame, text="Resultados exibidos com sucesso!", 
                    font=('Segoe UI', 14), bg=CORES["bg_accent"], fg=CORES["text_primary"]).pack(pady=20)

    def _criar_item_resultado(self, parent, index, resposta):
        """Criar item de resultado"""
        item_frame = tk.Frame(parent, bg=CORES["bg_secondary"], relief='solid', bd=1)
        item_frame.pack(fill='x', pady=8, padx=12)

        status = "✅ CORRETO" if resposta["acertou"] else "❌ INCORRETO"
        cor = CORES["accent_green"] if resposta["acertou"] else CORES["accent_red"]

        tk.Label(item_frame, text=f"{index+1}. {status}", 
                font=('Segoe UI', 16, 'bold'), bg=CORES["bg_secondary"], fg=cor).pack(anchor='w', padx=18, pady=10)

        tk.Label(item_frame, text=f"Pergunta: {resposta['pergunta']}", 
                font=('Segoe UI', 12), bg=CORES["bg_secondary"], fg=CORES["text_primary"], 
                wraplength=750).pack(anchor='w', padx=30)

        tk.Label(item_frame, text=f"Resposta correta: {resposta['resposta_correta']}", 
                font=('Segoe UI', 12), bg=CORES["bg_secondary"], fg=CORES["accent_green"]).pack(anchor='w', padx=30)

        tk.Label(item_frame, text=f"Sua resposta: {resposta['resposta_usuario']}", 
                font=('Segoe UI', 12), bg=CORES["bg_secondary"], fg=CORES["text_secondary"]).pack(anchor='w', padx=30)

        tk.Label(item_frame, text=f"Tentativas usadas: {resposta['tentativas_usadas']}", 
                font=('Segoe UI', 12), bg=CORES["bg_secondary"], fg=CORES["accent_orange"]).pack(anchor='w', padx=30, pady=(0,10))

    def _criar_botoes_navegacao_final(self, parent):
        """Criar botões de navegação final"""
        navegacao_frame = tk.Frame(parent, bg=CORES["bg_primary"])
        navegacao_frame.pack(side='bottom', fill='x', pady=25)

        tk.Label(navegacao_frame, text="Escolha sua próxima ação:", 
                font=('Segoe UI', 16), bg=CORES["bg_primary"], fg=CORES["text_secondary"]).pack(pady=12)

        botoes_navegacao_frame = tk.Frame(navegacao_frame, bg=CORES["bg_primary"])
        botoes_navegacao_frame.pack(pady=15)

        btn_recomecar = tk.Button(botoes_navegacao_frame, text="🔄 RECOMEÇAR AVENTURA", 
                                 command=self.callback_recomecar,
                                 font=('Segoe UI', 20, 'bold'), 
                                 bg=CORES["accent_green"], fg="white", relief='flat',
                                 padx=60, pady=35, cursor='hand2', width=20, height=2)
        btn_recomecar.pack(side='left', padx=30)

        btn_lobby = tk.Button(botoes_navegacao_frame, text="🏠 RETORNAR AO LOBBY", 
                             command=self.callback_menu,
                             font=('Segoe UI', 20, 'bold'), 
                             bg=CORES["accent_blue"], fg="white", relief='flat',
                             padx=60, pady=35, cursor='hand2', width=20, height=2)
        btn_lobby.pack(side='left', padx=30)
