FROM node:20
WORKDIR /app

# Install deps
COPY package.json package-lock.json* ./
RUN npm install --silent

# Copy source
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
