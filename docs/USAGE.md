# 📖 Guia de Uso - David-IAS

**CEO e Criador**: David Adriano Ferrari dos Santos

## Interface de Usuário

### Layout Principal

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 David-IAS  |  Modelo: mistral  |  ⚙️  🗑️              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Área de Chat                                                │
│                                                               │
│  👤 Usuário: Qual é o significado da vida?                │
│  🤖 IA: O significado da vida...                           │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  [Digite aqui...]                                     [📤]   │
│  ✅ Sistema Online                                          │
└─────────────────────────────────────────────────────────────┘
```

### Funcionalidades

#### 1. Chat Interativo

- Digite sua mensagem na caixa de entrada
- Clique em "Enviar" ou pressione Enter
- A IA responderá em tempo real

#### 2. Seleção de Modelo

- Clique no botão ⚙️ (Configurações)
- Escolha um modelo na lista
- O modelo será alterado imediatamente

#### 3. Gerenciamento de Histórico

- Clique no botão 🗑️ (Limpar) para apagar o histórico
- O histórico será limpo completamente

#### 4. Indicadores de Status

- 🟢 Conectado: Sistema está online e pronto
- 🔴 Desconectado: Verifique se Ollama está rodando

## Exemplos de Uso

### Chat Simples

```
Você: Olá, tudo bem?
IA: Olá! Tudo bem sim, e com você?
```

### Perguntas Técnicas

```
Você: Como fazer um loop em Python?
IA: Um loop em Python pode ser feito com 'for' ou 'while':
    
    for i in range(10):
        print(i)
    
    ou
    
    while i < 10:
        i += 1
```

### Análise e Resumos

```
Você: Resuma o seguinte texto: [copie aqui]
IA: [Fornecerá um resumo]
```

## Dicas e Truques

1. **Contexto**: A IA mantém o histórico da conversa
2. **Temperatura**: Valores mais altos = respostas mais criativas
3. **Modelos**: Diferentes modelos têm força em tarefas diferentes
4. **Prompt**: Seja específico e claro nas suas perguntas

## Modelos Recomendados

### Para Chat

```
neural-chat:latest
```
- Otimizado para conversas naturais
- Melhor compreensão de contexto

### Para Tarefas Técnicas

```
mistral:latest
```
- Versátil e rápido
- Bom para programação e análise

### Para Criatividade

```
dolphin-phi:latest
```
- Leve e criativo
- Bom para geração de texto

## Solução de Problemas

### "Sistema Desconectado"

**Problema**: Botão mostra desconectado

**Solução**:
1. Abra um terminal
2. Execute: `ollama serve`
3. Aguarde a conexão ser estabelecida

### "Timeout na Resposta"

**Problema**: A IA demora muito ou não responde

**Solução**:
1. Tente uma pergunta mais simples
2. Aumente o timeout no backend
3. Verifique a RAM disponível

### "Modelo não encontrado"

**Problema**: Erro ao selecionar modelo

**Solução**:
1. Baixe o modelo: `ollama pull [modelo]`
2. Aguarde o download
3. Selecione novamente

## Performance

### Otimização

- Use modelos menores para respostas mais rápidas
- Feche outras aplicações para liberar RAM
- Limpe o histórico periodicamente

### Requisitos

- **RAM**: 8GB mínimo (16GB recomendado)
- **Espaço**: 20GB para modelos
- **CPU**: Processador multi-core recomendado

## Atalhos de Teclado

| Atalho | Função |
|--------|--------|
| Enter | Enviar mensagem |
| Shift+Enter | Nova linha |
| Esc | Focar na caixa de entrada |

## Exportar Histórico

(Funcionalidade futura)

O histórico pode ser salvo em formato JSON para análise posterior.

## Próximas Funcionalidades

- [ ] Exportar conversas
- [ ] Temas personalizados
- [ ] Múltiplas abas de chat
- [ ] Integração com documentos
- [ ] Voz para texto
- [ ] Tradução de idiomas

---

**Desenvolvido com ❤️ por David Adriano Ferrari dos Santos**
