
"""
Lógica principal do jogo RPG Educativo
"""

import random
from config import CONFIGURACOES_PADRAO
from utils import mostrar_popup, mostrar_popup_questao

class LogicaJogo:
    def __init__(self, gerenciador_perguntas, configuracoes=None):
        self.gerenciador_perguntas = gerenciador_perguntas
        self.configuracoes = configuracoes or CONFIGURACOES_PADRAO.copy()
        self.reset_jogo()
        
    def reset_jogo(self):
        """Reset dos dados do jogo"""
        self.respostas_usuario = []
        self.tentativas_restantes = 0
        self.pergunta_atual = 0
        
    def iniciar_jogo(self):
        """Iniciar novo jogo"""
        if self.gerenciador_perguntas.total_perguntas() == 0:
            return False, "Adicione pelo menos uma pergunta para começar!"
            
        self.gerenciador_perguntas.preparar_perguntas_jogo(
            self.configuracoes["ordem_aleatoria"]
        )
        self.reset_jogo()
        return True, "Jogo iniciado com sucesso!"
        
    def obter_pergunta_atual(self):
        """Obter pergunta atual"""
        return self.gerenciador_perguntas.obter_pergunta(self.pergunta_atual)
        
    def tem_mais_perguntas(self):
        """Verificar se há mais perguntas"""
        return self.pergunta_atual < self.gerenciador_perguntas.total_perguntas_jogo()
        
    def inicializar_tentativas(self):
        """Inicializar tentativas para pergunta atual"""
        pergunta_config = self.obter_pergunta_atual()
        if pergunta_config:
            self.tentativas_restantes = (
                pergunta_config.get("tentativas_custom") or 
                self.configuracoes["num_tentativas"]
            )
        
    def verificar_resposta(self, resposta_usuario, parent=None):
        """Verificar resposta do usuário"""
        pergunta_config = self.obter_pergunta_atual()
        if not pergunta_config:
            return False, "Erro: pergunta não encontrada"
            
        resposta_correta = pergunta_config["resposta"]
        
        if resposta_usuario.lower().strip() == resposta_correta.lower().strip():
            return self._processar_resposta_correta(
                resposta_usuario, resposta_correta, pergunta_config, parent
            )
        else:
            return self._processar_resposta_incorreta(
                resposta_usuario, resposta_correta, pergunta_config, parent
            )
            
    def _processar_resposta_correta(self, resposta_usuario, resposta_correta, pergunta_config, parent):
        """Processar resposta correta"""
        self.respostas_usuario.append({
            "pergunta": pergunta_config["pergunta"],
            "resposta_correta": resposta_correta,
            "resposta_usuario": resposta_usuario,
            "acertou": True,
            "tentativas_usadas": self.configuracoes["num_tentativas"] - self.tentativas_restantes + 1
        })
        
        if parent:
            mostrar_popup(parent, "🎉 Correto!", 
                         "Excelente! Você acertou!\nAvançando para próxima pergunta...", "success")
        
        self.pergunta_atual += 1
        return True, "Resposta correta!"
        
    def _processar_resposta_incorreta(self, resposta_usuario, resposta_correta, pergunta_config, parent):
        """Processar resposta incorreta"""
        self.tentativas_restantes -= 1
        
        if self.tentativas_restantes > 0:
            dica_texto = self._obter_dica_tentativa(pergunta_config)
            mensagem = f"Resposta incorreta!\nTentativas restantes: {self.tentativas_restantes}{dica_texto}"
            
            if parent:
                mostrar_popup(parent, "❌ Incorreto", mensagem, "warning")
            
            return False, mensagem
        else:
            return self._processar_fim_tentativas(
                resposta_usuario, resposta_correta, pergunta_config, parent
            )
            
    def _processar_fim_tentativas(self, resposta_usuario, resposta_correta, pergunta_config, parent):
        """Processar fim de tentativas"""
        self.respostas_usuario.append({
            "pergunta": pergunta_config["pergunta"],
            "resposta_correta": resposta_correta,
            "resposta_usuario": resposta_usuario,
            "acertou": False,
            "tentativas_usadas": self.configuracoes["num_tentativas"]
        })
        
        mensagem = f"Tentativas esgotadas!\nA resposta correta era: {resposta_correta}"
        
        if parent:
            mostrar_popup(parent, "😞 Fim das Tentativas", mensagem, "error")
        
        self.pergunta_atual += 1
        return False, mensagem
        
    def _obter_dica_tentativa(self, pergunta_config):
        """Obter dica baseada na tentativa atual"""
        dica_texto = ""
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
                    
        return dica_texto
        
    def obter_dica_aleatoria(self, parent=None):
        """Obter dica aleatória para pergunta atual"""
        pergunta_config = self.obter_pergunta_atual()
        if not pergunta_config:
            return False, "Erro: pergunta não encontrada"
            
        dicas = pergunta_config.get("dicas", [])
        if not dicas and pergunta_config.get("dica"):
            dicas = [pergunta_config["dica"]]
            
        if dicas:
            dica_selecionada = random.choice(dicas)
            if parent:
                mostrar_popup(parent, "💡 Dica", 
                             f"Aqui está uma dica para você:\n\n{dica_selecionada}", "info")
            return True, dica_selecionada
        else:
            if parent:
                mostrar_popup(parent, "⚠️ Sem Dicas", 
                             "Não há dicas disponíveis para esta pergunta.", "warning")
            return False, "Sem dicas disponíveis"
            
    def deve_mostrar_dicas(self):
        """Verificar se deve mostrar dicas"""
        pergunta_config = self.obter_pergunta_atual()
        if not pergunta_config:
            return False
            
        mostrar_dicas = self.configuracoes["dicas_ativadas"]
        if pergunta_config.get("dicas_custom") is not None:
            mostrar_dicas = pergunta_config["dicas_custom"]
            
        dicas = pergunta_config.get("dicas", [])
        if not dicas and pergunta_config.get("dica"):
            dicas = [pergunta_config["dica"]]
            
        return mostrar_dicas and bool(dicas)
        
    def calcular_estatisticas(self):
        """Calcular estatísticas do jogo"""
        if not self.respostas_usuario:
            return {"acertos": 0, "total": 0, "porcentagem": 0}
            
        acertos = sum(1 for r in self.respostas_usuario if r["acertou"])
        total = len(self.respostas_usuario)
        porcentagem = (acertos / total) * 100 if total > 0 else 0
        
        return {
            "acertos": acertos,
            "total": total,
            "porcentagem": porcentagem
        }
        
    def recomecar_jogo(self, parent=None):
        """Recomeçar jogo"""
        if self.gerenciador_perguntas.total_perguntas() == 0:
            if parent:
                mostrar_popup(parent, "⚠️ Atenção", 
                             "Não há perguntas para recomeçar!", "warning")
            return False, "Sem perguntas disponíveis"
            
        if parent:
            resultado = mostrar_popup_questao(parent, "🔄 Recomeçar Aventura", 
                                            "Deseja recomeçar a aventura com as mesmas perguntas?")
            if not resultado:
                return False, "Cancelado pelo usuário"
                
        self.reset_jogo()
        self.gerenciador_perguntas.preparar_perguntas_jogo(
            self.configuracoes["ordem_aleatoria"]
        )
        return True, "Jogo reiniciado!"
        
    def obter_numero_pergunta_atual(self):
        """Obter número da pergunta atual (1-indexed)"""
        return self.pergunta_atual + 1
        
    def obter_total_perguntas_jogo(self):
        """Obter total de perguntas do jogo"""
        return self.gerenciador_perguntas.total_perguntas_jogo()
        
    def jogo_finalizado(self):
        """Verificar se o jogo foi finalizado"""
        return not self.tem_mais_perguntas()
