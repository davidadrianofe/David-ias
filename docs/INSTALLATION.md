# 📦 Guia de Instalação - David-IAS

**CEO e Criador**: David Adriano Ferrari dos Santos

## Pré-requisitos

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)
- **RAM**: Mínimo 8GB (recomendado 16GB+)
- **Espaço em disco**: 20GB para modelos

## Instalação Passo a Passo

### 1. Clone o Repositório

```bash
git clone https://github.com/davidadrianofe/David-ias.git
cd David-ias
```

### 2. Instale Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
- Baixe em https://ollama.ai
- Execute o instalador

### 3. Inicie Ollama

```bash
ollama serve
```

Deixe este terminal aberto. Ollama estará disponível em `http://localhost:11434`

### 4. Baixe um Modelo (em outro terminal)

```bash
# Recomendado: Mistral (rápido e eficiente)
ollama pull mistral:latest

# Alternativas:
ollama pull neural-chat:latest      # Ótimo para chat
ollama pull llama2:latest           # Mais poderoso
ollama pull dolphin-phi:latest      # Leve e rápido
```

### 5. Configure o Backend

```bash
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Crie arquivo .env
cp .env.example .env

# Edite .env se necessário
# nano .env (ou use seu editor favorito)
```

### 6. Inicie o Backend

```bash
# Certifique-se de que está na pasta backend e o venv está ativo
python main.py

# Você deve ver:
# 🚀 Iniciando servidor em 0.0.0.0:8000
```

### 7. Configure o Frontend

```bash
# Em um novo terminal, vá para a pasta frontend
cd frontend

# Instale dependências
npm install

# Inicie o servidor de desenvolvimento
npm start

# O navegador abrirá automaticamente em http://localhost:3000
```

## ✅ Verificação de Funcionamento

1. **Ollama**: http://localhost:11434 (deve retornar 404 - é normal)
2. **API Backend**: http://localhost:8000 (deve mostrar status)
3. **Frontend**: http://localhost:3000 (interface web)

## 🐳 Instalação com Docker

Se preferir usar Docker:

```bash
# Certifique-se de ter Docker e Docker Compose instalados

# Build das imagens
docker-compose build

# Inicie os serviços
docker-compose up -d

# Acesse em http://localhost:3000
```

## 🔧 Solução de Problemas

### Ollama não conecta

```bash
# Verifique se Ollama está rodando
curl http://localhost:11434/api/tags

# Se não funcionar, inicie Ollama
ollama serve
```

### Backend não inicia

```bash
# Certifique-se que está no ambiente virtual
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Tente instalar as dependências novamente
pip install -r requirements.txt --force-reinstall
```

### Frontend não conecta ao backend

```bash
# Abra o console do navegador (F12)
# Verifique se há erros CORS
# Certifique-se que o backend está rodando na porta 8000
```

### Erro "Modelo não encontrado"

```bash
# Liste os modelos disponíveis
ollama list

# Se não houver modelos, baixe um
ollama pull mistral:latest
```

## 📚 Próximos Passos

- Consulte [API.md](./API.md) para documentação da API
- Veja [USAGE.md](./USAGE.md) para guia de uso
- Leia [DEPLOYMENT.md](./DEPLOYMENT.md) para deploy em produção

---

**Precisando de ajuda? Abra uma issue no repositório!**
