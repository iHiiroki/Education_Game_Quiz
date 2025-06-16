
"""
Configurações globais do RPG Educativo
"""

# Configurações padrão do jogo
CONFIGURACOES_PADRAO = {
    "dicas_ativadas": True,
    "num_tentativas": 2,
    "ordem_aleatoria": False
}

# Temas disponíveis
TEMAS_DISPONIVEIS = [
    "Matemática", "Física", "História", "Geografia", 
    "Ciências", "Literatura", "Inglês", "Personalizado"
]

# Paleta de cores moderna
CORES = {
    "bg_primary": "#1a252f",
    "bg_secondary": "#2c3e50",
    "bg_accent": "#34495e",
    "bg_card": "#2d3748",
    "bg_input": "#1a202c",
    "text_primary": "#ecf0f1",
    "text_secondary": "#bdc3c7",
    "accent_blue": "#3498db",
    "accent_green": "#2ecc71",
    "accent_red": "#e74c3c",
    "accent_orange": "#f39c12",
    "accent_purple": "#9b59b6",
    "accent_yellow": "#f1c40f"
}

# Cores hover para botões
CORES_HOVER = {
    "#3498db": "#5dade2",
    "#2ecc71": "#58d68d",
    "#e74c3c": "#ec7063",
    "#f39c12": "#f8c471",
    "#9b59b6": "#bb8fce"
}

# Configurações de janela
JANELA_CONFIG = {
    "titulo": "RPG Educativo - Aventura do Conhecimento",
    "geometria": "1100x800",
    "min_size": (700, 700)
}

# Configurações de popup
POPUP_CONFIG = {
    "geometria": "450x280",
    "icones": {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠",
        "error": "❌",
        "question": "❓"
    }
}

# Configurações de dificuldade
DIFICULDADES = {
    "facil": {"pontos": 10, "cor": "#27ae60"},
    "medio": {"pontos": 20, "cor": "#f39c12"},
    "dificil": {"pontos": 30, "cor": "#e74c3c"}
}
