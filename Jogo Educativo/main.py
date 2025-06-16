
"""
RPG Educativo - Aventura do Conhecimento
Ponto de entrada principal do jogo
"""

from interface import JogoEducativoRPG

if __name__ == "__main__":
    try:
        jogo = JogoEducativoRPG()
        jogo.executar()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
        import tkinter.messagebox as mb
        mb.showerror("Erro", f"Erro ao iniciar o jogo: {e}")
