"""
LLM Manager - Gerenciador de Inteligência Artificial Local
Integração com Ollama para modelos LLM locais
"""

import requests
import os
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LLMManager:
    """Gerenciador de LLM Local usando Ollama"""
    
    def __init__(self):
        """Inicializa o gerenciador de LLM"""
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.current_model = os.getenv("OLLAMA_MODEL", "mistral:latest")
        self.history: List[Dict] = []
        self.session_tokens = 0
        
        # Testa conexão com Ollama
        if not self.is_connected():
            logger.warning("⚠️ Ollama não está acessível. Certifique-se de que está rodando.")
            logger.info("Para iniciar Ollama, execute: ollama serve")
        else:
            logger.info("✅ Conectado a Ollama com sucesso")
    
    def is_connected(self) -> bool:
        """Verifica se está conectado ao Ollama"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Erro ao conectar com Ollama: {e}")
            return False
    
    def list_models(self) -> List[Dict]:
        """Lista os modelos disponíveis no Ollama"""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags")
            
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get("models", []):
                    models.append({
                        "name": model["name"],
                        "size": self._format_size(model.get("size", 0)),
                        "description": f"Modelo: {model['name']}",
                        "modified_at": model.get("modified_at")
                    })
                return models
            else:
                logger.error(f"Erro ao listar modelos: {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Erro ao conectar com Ollama: {e}")
            return []
    
    def switch_model(self, model_name: str) -> bool:
        """Muda o modelo LLM"""
        try:
            # Testa se o modelo existe fazendo uma requisição rápida
            response = requests.post(
                f"{self.ollama_host}/api/show",
                json={"name": model_name},
                timeout=5
            )
            
            if response.status_code == 200:
                self.current_model = model_name
                logger.info(f"Modelo alterado para: {model_name}")
                self.history = []  # Limpa histórico ao trocar modelo
                return True
            else:
                logger.error(f"Modelo {model_name} não encontrado")
                return False
        except Exception as e:
            logger.error(f"Erro ao trocar modelo: {e}")
            return False
    
    def generate_response(self, message: str, model: Optional[str] = None, 
                         temperature: float = 0.7) -> Dict:
        """
        Gera uma resposta do LLM
        
        Args:
            message: Mensagem do usuário
            model: Modelo a usar (usa o padrão se não especificado)
            temperature: Temperatura (criatividade) da resposta
        
        Returns:
            Dict com resposta e metadados
        """
        if not self.is_connected():
            raise Exception("Ollama não está conectado. Inicie com: ollama serve")
        
        model_to_use = model or self.current_model
        
        try:
            # Adiciona mensagem do usuário ao histórico
            self.history.append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Cria contexto a partir do histórico
            context = self._build_context()
            
            # Faz requisição ao Ollama
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": model_to_use,
                    "prompt": context + "\n\nAssistant: ",
                    "stream": False,
                    "temperature": temperature,
                    "num_predict": 512
                },
                timeout=300  # 5 minutos de timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "").strip()
                
                # Remove "Assistant: " se estiver no início
                if response_text.startswith("Assistant:"):
                    response_text = response_text.replace("Assistant:", "", 1).strip()
                
                # Adiciona resposta ao histórico
                self.history.append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().isoformat()
                })
                
                tokens_used = data.get("eval_count", 0)
                self.session_tokens += tokens_used
                
                logger.info(f"✅ Resposta gerada - Modelo: {model_to_use}, Tokens: {tokens_used}")
                
                return {
                    "text": response_text,
                    "model": model_to_use,
                    "tokens_used": tokens_used,
                    "total_tokens": self.session_tokens
                }
            else:
                error_msg = f"Erro ao gerar resposta: {response.status_code}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.Timeout:
            logger.error("Timeout ao gerar resposta")
            raise Exception("Timeout - A resposta levou muito tempo para ser gerada")
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            raise Exception(f"Erro ao gerar resposta: {str(e)}")
    
    def get_history(self) -> List[Dict]:
        """Retorna o histórico de chat"""
        return self.history.copy()
    
    def clear_history(self):
        """Limpa o histórico de chat"""
        self.history = []
        self.session_tokens = 0
        logger.info("Histórico limpo")
    
    def _build_context(self, max_messages: int = 10) -> str:
        """Constrói o contexto para a próxima mensagem"""
        # Pega as últimas mensagens
        recent_history = self.history[-max_messages:]
        
        context_parts = []
        for msg in recent_history:
            role = msg["role"].capitalize()
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Formata tamanho em bytes para formato legível"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def close(self):
        """Fecha a conexão e limpa recursos"""
        logger.info("Encerrando LLM Manager")
        self.clear_history()
