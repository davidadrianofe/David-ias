"""
David-IAS - Backend FastAPI com LLM Local
CEO e Criador: David Adriano Ferrari dos Santos
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from llm_manager import LLMManager

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="David-IAS API",
    description="Sistema de IA LLM Local",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ChatMessage(BaseModel):
    role: str  # "user" ou "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = None
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    response: str
    model: str
    timestamp: datetime
    tokens_used: Optional[int] = None

class ModelInfo(BaseModel):
    name: str
    size: str
    description: str
    available: bool

# Gerenciador de LLM Global
llm_manager = None

@app.on_event("startup")
async def startup():
    """Inicializa o gerenciador de LLM"""
    global llm_manager
    try:
        llm_manager = LLMManager()
        logger.info("✅ LLM Manager inicializado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar LLM Manager: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    """Limpa recursos ao encerrar"""
    global llm_manager
    if llm_manager:
        llm_manager.close()
        logger.info("LLM Manager encerrado")

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "David-IAS",
        "version": "1.0.0",
        "creator": "David Adriano Ferrari dos Santos"
    }

@app.get("/api/status")
async def get_status():
    """Obter status do sistema"""
    if not llm_manager:
        raise HTTPException(status_code=503, detail="LLM Manager não inicializado")
    
    return {
        "status": "running",
        "ollama_connected": llm_manager.is_connected(),
        "current_model": llm_manager.current_model,
        "available_models": llm_manager.get_available_models(),
        "timestamp": datetime.now()
    }

@app.get("/api/models")
async def list_models() -> List[ModelInfo]:
    """Listar modelos disponíveis"""
    if not llm_manager:
        raise HTTPException(status_code=503, detail="LLM Manager não inicializado")
    
    models = llm_manager.list_models()
    return [
        ModelInfo(
            name=model["name"],
            size=model.get("size", "unknown"),
            description=model.get("description", ""),
            available=True
        )
        for model in models
    ]

@app.post("/api/models/switch")
async def switch_model(model_name: str):
    """Trocar modelo LLM"""
    if not llm_manager:
        raise HTTPException(status_code=503, detail="LLM Manager não inicializado")
    
    try:
        success = llm_manager.switch_model(model_name)
        if success:
            logger.info(f"Modelo alterado para: {model_name}")
            return {"status": "success", "current_model": model_name}
        else:
            raise HTTPException(status_code=400, detail=f"Modelo {model_name} não encontrado")
    except Exception as e:
        logger.error(f"Erro ao trocar modelo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """Enviar mensagem de chat"""
    if not llm_manager:
        raise HTTPException(status_code=503, detail="LLM Manager não inicializado")
    
    try:
        response = llm_manager.generate_response(
            message=request.message,
            model=request.model,
            temperature=request.temperature
        )
        
        logger.info(f"Chat processado com sucesso")
        
        return ChatResponse(
            response=response["text"],
            model=response["model"],
            timestamp=datetime.now(),
            tokens_used=response.get("tokens_used")
        )
    except Exception as e:
        logger.error(f"Erro ao processar chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history():
    """Obter histórico de chat"""
    if not llm_manager:
        raise HTTPException(status_code=503, detail="LLM Manager não inicializado")
    
    return {"history": llm_manager.get_history()}

@app.delete("/api/history")
async def clear_history():
    """Limpar histórico de chat"""
    if not llm_manager:
        raise HTTPException(status_code=503, detail="LLM Manager não inicializado")
    
    llm_manager.clear_history()
    return {"status": "success", "message": "Histórico limpo"}

@app.post("/api/reset")
async def reset_system():
    """Resetar sistema"""
    global llm_manager
    if llm_manager:
        llm_manager.close()
    llm_manager = LLMManager()
    return {"status": "success", "message": "Sistema resetado"}

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    logger.info(f"🚀 Iniciando servidor em {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
