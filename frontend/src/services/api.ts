/**
 * Serviço de API para comunicação com backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutos
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ChatRequest {
  message: string;
  model?: string;
  temperature?: number;
}

export interface ChatResponse {
  response: string;
  model: string;
  timestamp: string;
  tokens_used?: number;
}

export interface Model {
  name: string;
  size: string;
  description: string;
  available: boolean;
}

export interface SystemStatus {
  status: string;
  ollama_connected: boolean;
  current_model: string;
  available_models: string[];
  timestamp: string;
}

export const apiService = {
  /**
   * Obter status do sistema
   */
  async getStatus(): Promise<SystemStatus> {
    try {
      const response = await api.get<SystemStatus>('/api/status');
      return response.data;
    } catch (error) {
      throw new Error('Erro ao obter status do sistema');
    }
  },

  /**
   * Listar modelos disponíveis
   */
  async listModels(): Promise<Model[]> {
    try {
      const response = await api.get<Model[]>('/api/models');
      return response.data;
    } catch (error) {
      throw new Error('Erro ao listar modelos');
    }
  },

  /**
   * Trocar modelo LLM
   */
  async switchModel(modelName: string): Promise<{ status: string; current_model: string }> {
    try {
      const response = await api.post<{ status: string; current_model: string }>(
        '/api/models/switch',
        { model_name: modelName }
      );
      return response.data;
    } catch (error) {
      throw new Error('Erro ao trocar modelo');
    }
  },

  /**
   * Enviar mensagem de chat
   */
  async chat(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await api.post<ChatResponse>('/api/chat', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Erro ao processar chat');
      }
      throw error;
    }
  },

  /**
   * Obter histórico de chat
   */
  async getHistory(): Promise<{ history: any[] }> {
    try {
      const response = await api.get<{ history: any[] }>('/api/history');
      return response.data;
    } catch (error) {
      throw new Error('Erro ao obter histórico');
    }
  },

  /**
   * Limpar histórico de chat
   */
  async clearHistory(): Promise<{ status: string }> {
    try {
      const response = await api.delete<{ status: string }>('/api/history');
      return response.data;
    } catch (error) {
      throw new Error('Erro ao limpar histórico');
    }
  },

  /**
   * Resetar sistema
   */
  async resetSystem(): Promise<{ status: string; message: string }> {
    try {
      const response = await api.post<{ status: string; message: string }>('/api/reset');
      return response.data;
    } catch (error) {
      throw new Error('Erro ao resetar sistema');
    }
  },
};
