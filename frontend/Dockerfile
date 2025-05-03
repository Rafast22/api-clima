# Etapa 1: Construção do Angular
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
#RUN npm run build --configuration=production
RUN npm run build --prod

# Etapa 2: Configuração do Nginx
FROM nginx:latest
COPY --from=build /app/dist/front/browser/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]

