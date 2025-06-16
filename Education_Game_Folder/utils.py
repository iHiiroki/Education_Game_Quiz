
"""
Funções auxiliares para o RPG Educativo
"""

import tkinter as tk
from tkinter import messagebox
import random
from config import CORES, CORES_HOVER, POPUP_CONFIG

class PopupModerno:
    def __init__(self, parent, titulo, mensagem, tipo="info", callback=None):
        self.callback = callback
        self.resultado = None
        self.popup = tk.Toplevel(parent)
        self.popup.title(titulo)
        self.popup.geometry(POPUP_CONFIG["geometria"])
        self.popup.configure(bg=CORES["bg_secondary"])
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
        main_frame = tk.Frame(self.popup, bg=CORES["bg_accent"], relief='solid', bd=1)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)

        title_frame = tk.Frame(main_frame, bg=CORES["bg_secondary"], height=45)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        icone = POPUP_CONFIG["icones"].get(tipo, "ℹ️")

        tk.Label(title_frame, text=f"{icone} {titulo}", font=('Segoe UI', 13, 'bold'),
                bg=CORES["bg_secondary"], fg=CORES["text_primary"]).pack(side='left', padx=20, pady=12)

        tk.Button(title_frame, text="✕", font=('Segoe UI', 11, 'bold'),
                 bg=CORES["accent_red"], fg="white", relief='flat', width=3, height=1,
                 command=self.fechar).pack(side='right', padx=15, pady=10)

        content_frame = tk.Frame(main_frame, bg=CORES["bg_accent"])
        content_frame.pack(fill='both', expand=True, padx=25, pady=25)

        tk.Label(content_frame, text=mensagem, font=('Segoe UI', 12),
                bg=CORES["bg_accent"], fg=CORES["text_primary"], wraplength=380, justify='center').pack(pady=25)

        self.criar_botoes(content_frame, tipo)

    def criar_botoes(self, parent, tipo):
        botoes_frame = tk.Frame(parent, bg=CORES["bg_accent"])
        botoes_frame.pack(side='bottom', pady=15)

        if tipo == "question":
            tk.Button(botoes_frame, text="✅ SIM", font=('Segoe UI', 11, 'bold'),
                     bg=CORES["accent_green"], fg="white", relief='flat', padx=25, pady=8,
                     command=lambda: self.definir_resultado(True)).pack(side='left', padx=12)
            tk.Button(botoes_frame, text="❌ NÃO", font=('Segoe UI', 11, 'bold'),
                     bg=CORES["accent_red"], fg="white", relief='flat', padx=25, pady=8,
                     command=lambda: self.definir_resultado(False)).pack(side='left', padx=12)
        else:
            tk.Button(botoes_frame, text="✓ OK", font=('Segoe UI', 11, 'bold'),
                     bg=CORES["accent_blue"], fg="white", relief='flat', padx=35, pady=8,
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

def mostrar_popup(parent, titulo, mensagem, tipo="info"):
    """Função helper para mostrar popups"""
    try:
        return PopupModerno(parent, titulo, mensagem, tipo)
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

def mostrar_popup_questao(parent, titulo, mensagem):
    """Função helper para popups de pergunta"""
    try:
        popup = PopupModerno(parent, titulo, mensagem, "question")
        return popup.resultado
    except:
        return messagebox.askyesno(titulo, mensagem)

def criar_botao_moderno(parent, texto, comando, cor_bg, cor_fg="white"):
    """Criar botão com estilo moderno e hover"""
    btn = tk.Button(parent, text=texto, command=comando, font=('Segoe UI', 13, 'bold'), 
                   bg=cor_bg, fg=cor_fg, relief='flat', padx=35, pady=18, cursor='hand2')
    try:
        btn.bind("<Enter>", lambda e: btn.configure(bg=CORES_HOVER.get(cor_bg, cor_bg)))
        btn.bind("<Leave>", lambda e: btn.configure(bg=cor_bg))
    except:
        pass
    return btn

def clarear_cor(cor):
    """Obter cor mais clara para hover"""
    return CORES_HOVER.get(cor, cor)

def limpar_tela(root):
    """Limpar todos os widgets da tela"""
    try:
        for widget in root.winfo_children():
            widget.destroy()
    except:
        pass

def centralizar_janela(window):
    """Centralizar janela na tela"""
    try:
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    except:
        pass

def rolar_dado():
    """Rolar um dado de 6 lados"""
    return random.randint(1, 6)

def configurar_placeholder(entry, placeholder, cores):
    """Configurar placeholder para Entry"""
    entry.insert(0, placeholder)
    
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=cores["text_primary"])

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=cores["text_secondary"])

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def configurar_placeholder_text(text_widget, placeholder, cores):
    """Configurar placeholder para Text widget"""
    text_widget.insert("1.0", placeholder)
    
    def on_focus_in(event):
        content = text_widget.get("1.0", tk.END).strip()
        if content == placeholder:
            text_widget.delete("1.0", tk.END)
            text_widget.config(fg=cores["text_primary"])

    def on_focus_out(event):
        content = text_widget.get("1.0", tk.END).strip()
        if not content:
            text_widget.insert("1.0", placeholder)
            text_widget.config(fg=cores["text_secondary"])

    text_widget.bind("<FocusIn>", on_focus_in)
    text_widget.bind("<FocusOut>", on_focus_out)

def configurar_scroll_mouse(canvas):
    """Configurar scroll do mouse para canvas"""
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

    canvas.bind("<MouseWheel>", on_mousewheel)
    canvas.bind("<Button-4>", on_mousewheel_linux_up)
    canvas.bind("<Button-5>", on_mousewheel_linux_down)

    return on_mousewheel, on_mousewheel_linux_up, on_mousewheel_linux_down

def bind_scroll_to_children(widget, scroll_functions):
    """Aplicar scroll aos widgets filhos"""
    on_mousewheel, on_mousewheel_linux_up, on_mousewheel_linux_down = scroll_functions
    try:
        widget.bind("<MouseWheel>", on_mousewheel)
        widget.bind("<Button-4>", on_mousewheel_linux_up)
        widget.bind("<Button-5>", on_mousewheel_linux_down)
        for child in widget.winfo_children():
            bind_scroll_to_children(child, scroll_functions)
    except:
        pass
