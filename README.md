# 🤖 David-IAS - Sistema de IA LLM Local Completo

**CEO e Criador**: David Adriano Ferrari dos Santos

Sistema completo de Inteligência Artificial com LLM Local, Interface Web Profissional e Backend Robusto.

## 🎯 Características

- ✅ LLM Local (sem dependência de APIs externas)
- ✅ Interface Web Moderna e Responsiva
- ✅ Chat Interativo com Histórico
- ✅ Suporte a Múltiplos Modelos
- ✅ Backend em FastAPI (Python)
- ✅ Frontend em React/TypeScript
- ✅ Documentação Completa
- ✅ Fácil de Usar e Instalar

## 📋 Pré-requisitos

- Python 3.9+
- Node.js 18+
- Docker (opcional)
- 8GB de RAM mínimo
- 20GB de espaço em disco

## 🚀 Instalação Rápida

### Backend (Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend (React)

```bash
cd frontend
npm install
npm start
```

## 📦 Estrutura do Projeto

```
David-ias/
├── backend/
│   ├── main.py              # Servidor FastAPI
│   ├── models.py            # Modelos de dados
│   ├── llm_manager.py       # Gerenciador de LLM
│   ├── requirements.txt     # Dependências Python
│   └── .env.example         # Variáveis de ambiente
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/           # Páginas
│   │   ├── services/        # Serviços API
│   │   ├── styles/          # Estilos CSS
│   │   └── App.tsx          # App Principal
│   ├── package.json
│   └── tsconfig.json
├── docs/                    # Documentação
├── docker-compose.yml       # Docker Compose
└── README.md               # Este arquivo
```

## 🔧 Configuração

### 1. Variáveis de Ambiente

```bash
# backend/.env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:latest
API_PORT=8000
API_HOST=0.0.0.0
ENVIRONMENT=development
```

### 2. Instalar Ollama

```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Baixar em https://ollama.ai
```

### 3. Baixar Modelo

```bash
ollama pull mistral:latest
# ou
ollama pull neural-chat:latest
```

## 💻 Como Usar

### Iniciar o Sistema

```bash
# Terminal 1: Iniciar Ollama
ollama serve

# Terminal 2: Iniciar Backend
cd backend
python main.py

# Terminal 3: Iniciar Frontend
cd frontend
npm start
```

### Acessar a Interface

```
http://localhost:3000
```

## 🌐 API Endpoints

- `POST /api/chat` - Enviar mensagem de chat
- `GET /api/models` - Listar modelos disponíveis
- `POST /api/models/switch` - Trocar modelo
- `GET /api/history` - Obter histórico de chat
- `DELETE /api/history` - Limpar histórico
- `GET /api/status` - Status do sistema

## 📚 Documentação

Veja a pasta `/docs` para documentação completa:
- `INSTALLATION.md` - Guia de instalação detalhado
- `API.md` - Documentação da API
- `USAGE.md` - Guia de uso
- `DEPLOYMENT.md` - Deploy em produção

## 🐳 Docker

```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Acessar
http://localhost:3000
```

## 🎨 Interface

A interface inclui:
- Chat interativo em tempo real
- Seleção de modelos
- Histórico de conversas
- Tema claro/escuro
- Design responsivo
- Indicadores de status

## 📄 Licença

© 2024 David Adriano Ferrari dos Santos. Todos os direitos reservados.

## 🤝 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Desenvolvido com ❤️ por David Adriano Ferrari dos Santos**
