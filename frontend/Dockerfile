FROM node:18-alpine as builder

WORKDIR /app

# Copia package files
COPY package*.json ./

# Instala dependências
RUN npm ci

# Copia código
COPY . .

# Build
RUN npm run build

# Production
FROM node:18-alpine

WORKDIR /app

# Instala serve para servir arquivos estáticos
RUN npm install -g serve

# Copia arquivos built do estágio anterior
COPY --from=builder /app/dist ./dist

# Expõe porta
EXPOSE 3000

# Define variáveis de ambiente
ENV VITE_API_URL=http://localhost:8000

# Inicia servidor
CMD ["serve", "-s", "dist", "-l", "3000"]
