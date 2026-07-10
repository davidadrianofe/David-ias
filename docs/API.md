# 📡 Documentação da API - David-IAS

**Base URL**: `http://localhost:8000`

## Autenticação

Atualmente, a API não requer autenticação. Em produção, considere adicionar JWT ou OAuth.

## Endpoints

### 1. Health Check

#### GET `/`

Verifica se o servidor está online.

**Resposta (200):**
```json
{
  "status": "online",
  "service": "David-IAS",
  "version": "1.0.0",
  "creator": "David Adriano Ferrari dos Santos"
}
```

---

### 2. Status do Sistema

#### GET `/api/status`

Obtém o status atual do sistema e conexão com Ollama.

**Resposta (200):**
```json
{
  "status": "running",
  "ollama_connected": true,
  "current_model": "mistral:latest",
  "available_models": ["mistral:latest", "neural-chat:latest"],
  "timestamp": "2024-01-10T15:30:00"
}
```

**Respostas de erro:**
- `503`: LLM Manager não inicializado

---

### 3. Listar Modelos

#### GET `/api/models`

Retorna lista de modelos disponíveis no Ollama.

**Resposta (200):**
```json
[
  {
    "name": "mistral:latest",
    "size": "3.97 GB",
    "description": "Modelo: mistral:latest",
    "available": true
  },
  {
    "name": "neural-chat:latest",
    "size": "4.07 GB",
    "description": "Modelo: neural-chat:latest",
    "available": true
  }
]
```

**Respostas de erro:**
- `503`: LLM Manager não inicializado

---

### 4. Trocar Modelo

#### POST `/api/models/switch`

Altera o modelo LLM atual.

**Body:**
```json
{
  "model_name": "neural-chat:latest"
}
```

**Resposta (200):**
```json
{
  "status": "success",
  "current_model": "neural-chat:latest"
}
```

**Respostas de erro:**
- `400`: Modelo não encontrado
- `500`: Erro ao trocar modelo
- `503`: LLM Manager não inicializado

---

### 5. Enviar Mensagem de Chat

#### POST `/api/chat`

Envia uma mensagem e obtém resposta da IA.

**Body:**
```json
{
  "message": "Olá, como você está?",
  "model": "mistral:latest",
  "temperature": 0.7
}
```

**Parâmetros:**
- `message` (string, obrigatório): Mensagem do usuário
- `model` (string, opcional): Modelo a usar (usa o padrão se omitido)
- `temperature` (number, opcional): Controla criatividade (0.0-1.0, padrão: 0.7)

**Resposta (200):**
```json
{
  "response": "Olá! Estou bem, obrigado por perguntar. Como posso ajudá-lo?",
  "model": "mistral:latest",
  "timestamp": "2024-01-10T15:30:00",
  "tokens_used": 45
}
```

**Respostas de erro:**
- `500`: Erro ao gerar resposta
- `503`: LLM Manager não inicializado

---

### 6. Obter Histórico de Chat

#### GET `/api/history`

Retorna o histórico completo de conversas.

**Resposta (200):**
```json
{
  "history": [
    {
      "role": "user",
      "content": "Olá",
      "timestamp": "2024-01-10T15:30:00"
    },
    {
      "role": "assistant",
      "content": "Oi! Como posso ajudar?",
      "timestamp": "2024-01-10T15:30:05"
    }
  ]
}
```

**Respostas de erro:**
- `503`: LLM Manager não inicializado

---

### 7. Limpar Histórico

#### DELETE `/api/history`

Remove todo o histórico de conversas.

**Resposta (200):**
```json
{
  "status": "success",
  "message": "Histórico limpo"
}
```

**Respostas de erro:**
- `503`: LLM Manager não inicializado

---

### 8. Resetar Sistema

#### POST `/api/reset`

Reinicializa completamente o sistema.

**Resposta (200):**
```json
{
  "status": "success",
  "message": "Sistema resetado"
}
```

---

## Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 404 | Não encontrado |
| 500 | Erro interno do servidor |
| 503 | Serviço indisponível |

---

## Exemplos de Uso

### cURL

```bash
# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "O que é inteligência artificial?",
    "temperature": 0.7
  }'

# Listar modelos
curl http://localhost:8000/api/models

# Status
curl http://localhost:8000/api/status
```

### JavaScript/TypeScript

```typescript
// Chat
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Qual é o significado da vida?",
    temperature: 0.7
  })
});

const data = await response.json();
console.log(data.response);
```

### Python

```python
import requests

# Chat
response = requests.post('http://localhost:8000/api/chat', json={
    'message': 'Olá!',
    'temperature': 0.7
})

print(response.json()['response'])
```

---

## Rate Limiting

Atualmente não há rate limiting. Para produção, considere implementar.

## CORS

CORS está habilitado para todas as origens (`*`). Para produção, restrinja a origens específicas.

---

## Versão

- **Versão da API**: 1.0.0
- **Data**: Janeiro de 2024
- **Creator**: David Adriano Ferrari dos Santos
