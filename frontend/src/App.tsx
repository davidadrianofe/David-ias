/**
 * David-IAS - Frontend Principal
 * CEO e Criador: David Adriano Ferrari dos Santos
 */

import React, { useState, useEffect, useRef } from 'react';
import { Send, Settings, Trash2, Loader, AlertCircle, Check } from 'lucide-react';
import './styles/App.css';
import { apiService } from './services/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface SystemStatus {
  status: string;
  ollama_connected: boolean;
  current_model: string;
  available_models: string[];
}

export function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState<string[]>([]);
  const [currentModel, setCurrentModel] = useState('mistral:latest');
  const [showSettings, setShowSettings] = useState(false);
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll para a última mensagem
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Carrega status e modelos ao iniciar
  useEffect(() => {
    loadStatus();
    loadModels();
    const interval = setInterval(loadStatus, 5000); // Atualiza status a cada 5s
    return () => clearInterval(interval);
  }, []);

  const loadStatus = async () => {
    try {
      const data = await apiService.getStatus();
      setStatus(data);
      setError(null);
    } catch (err) {
      setError('Erro ao conectar com o servidor');
      console.error(err);
    }
  };

  const loadModels = async () => {
    try {
      const modelList = await apiService.listModels();
      const modelNames = modelList.map(m => m.name);
      setModels(modelNames);
      if (modelNames.length > 0 && !modelNames.includes(currentModel)) {
        setCurrentModel(modelNames[0]);
      }
    } catch (err) {
      console.error('Erro ao carregar modelos:', err);
      setError('Erro ao carregar modelos');
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.chat({
        message: input,
        model: currentModel,
        temperature: 0.7
      });

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      setError('Erro ao enviar mensagem: ' + (err as Error).message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      await apiService.clearHistory();
      setMessages([]);
      setError(null);
    } catch (err) {
      setError('Erro ao limpar histórico');
      console.error(err);
    }
  };

  const handleSwitchModel = async (modelName: string) => {
    try {
      await apiService.switchModel(modelName);
      setCurrentModel(modelName);
      setError(null);
    } catch (err) {
      setError('Erro ao trocar modelo');
      console.error(err);
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <h1 className="app-title">🤖 David-IAS</h1>
            <p className="app-subtitle">IA LLM Local</p>
          </div>
          <div className="header-controls">
            <button
              className="icon-button settings-button"
              onClick={() => setShowSettings(!showSettings)}
              title="Configurações"
            >
              <Settings size={20} />
            </button>
            <button
              className="icon-button clear-button"
              onClick={handleClearHistory}
              title="Limpar histórico"
            >
              <Trash2 size={20} />
            </button>
          </div>
        </div>

        {/* Status Bar */}
        <div className="status-bar">
          <div className="status-item">
            <span className={`status-indicator ${status?.ollama_connected ? 'connected' : 'disconnected'}`}></span>
            <span>{status?.ollama_connected ? 'Conectado' : 'Desconectado'}</span>
          </div>
          <div className="status-item">
            <span className="status-label">Modelo:</span>
            <span className="status-value">{currentModel}</span>
          </div>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="settings-panel">
            <h3>Configurações</h3>
            <div className="settings-group">
              <label>Selecione o Modelo:</label>
              <select
                value={currentModel}
                onChange={(e) => handleSwitchModel(e.target.value)}
                className="model-select"
              >
                {models.map(model => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </div>
            <div className="settings-info">
              <p>Modelos disponíveis: {models.length}</p>
              <p>Status: {status?.status}</p>
            </div>
          </div>
        )}
      </header>

      {/* Main Chat Area */}
      <main className="chat-container">
        <div className="messages-list">
          {messages.length === 0 && (
            <div className="empty-state">
              <div className="empty-icon">🤖</div>
              <h2>Bem-vindo ao David-IAS</h2>
              <p>Comece uma conversa com a IA</p>
              <p className="creator-info">CEO e Criador: David Adriano Ferrari dos Santos</p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-wrapper message-${message.role}`}
            >
              <div className="message-content">
                <div className="message-role">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-text">
                  {message.content}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-wrapper message-assistant">
              <div className="message-content">
                <div className="message-role">🤖</div>
                <div className="message-text loading">
                  <Loader size={16} className="spinner" />
                  Processando...
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Error Message */}
      {error && (
        <div className="error-banner">
          <AlertCircle size={20} />
          <span>{error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* Input Area */}
      <footer className="input-footer">
        <form onSubmit={handleSendMessage} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Digite sua mensagem..."
            className="message-input"
            disabled={loading || !status?.ollama_connected}
          />
          <button
            type="submit"
            disabled={loading || !input.trim() || !status?.ollama_connected}
            className="send-button"
            title="Enviar mensagem"
          >
            {loading ? (
              <Loader size={20} className="spinner" />
            ) : (
              <Send size={20} />
            )}
          </button>
        </form>
        <p className="footer-info">
          {status?.ollama_connected ? '✅ Sistema Online' : '❌ Aguardando conexão'}
        </p>
      </footer>
    </div>
  );
}

export default App;
