# ---- Build Stage ----
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# ---- Production Stage ----
FROM node:20-alpine

WORKDIR /app

RUN adduser -D appuser

COPY --from=builder /app ./

USER appuser

HEALTHCHECK CMD wget --spider http://localhost:3000 || exit 1

CMD ["npm", "start"]