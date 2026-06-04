# Builder slika: slika koja gradi našu sliku. Te dvije slike imaju različit sadržaj.
# Primjerice, slika koja gradi zahtijeva Node jer pokreće `npm`, a naša konačna slika ne treba Node jer ne pokreće `npm`. Prva slika ne treba `nginx`, a druga slika terba `nginx`.
FROM node:25-alpine AS builder

WORKDIR /app
# Kopiramo cijeli frontend direktorij (trenutni) u sliku.
COPY . .
# Slično kao npm install, ali bez ignoriranja inkonzistentnosti između package.json i package-lock.json.
RUN npm ci

# Moramo navesti koje environment varijable koristimo.
ARG VITE_CLIENT_ID
ARG VITE_TENANT_ID
# Sada možemo kompajlirati frontend; datoteke će biti stvorene u `dist` direktoriju unutar ove (pomoćne) slike.
RUN npm run build

FROM nginx:alpine
# U finalnoj slici trebamo samo kompajlirane datoteke, dakle `/app/dist` iz *builder* slike.
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/templates/default.conf.template

# U nginx.confg koristimo referencu na BACKEND_HOST; ovdje definiramo njenu vrijednost.
ENV BACKEND_HOST=localhost

EXPOSE 80
