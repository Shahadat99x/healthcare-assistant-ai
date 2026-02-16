# ──────────────────────────────────────────────
# Healthcare Assistant AI — Web (Next.js)
# ──────────────────────────────────────────────
FROM node:20-slim

WORKDIR /app

# Install dependencies first (layer cache)
COPY package.json package-lock.json ./
RUN npm ci

# Copy application code
COPY . .

EXPOSE 3000

# Use dev server for docker-compose (hot reload)
CMD ["npm", "run", "dev"]
