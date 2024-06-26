# Stage 1: Build
# Utiliza la imagen oficial de Node.js como base
FROM node:alpine AS builder

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias y construye la aplicación
RUN npm install
RUN npm run build --prod

# Stage 2
# Utiliza la imagen oficial de Nginx como base para el servidor web
FROM nginx:alpine

# Copia los archivos de la aplicación compilada al directorio de Nginx
COPY --from=builder  /usr/src/app/dist/ecommerce-app /usr/share/nginx/html
# configuracion de nginx dentro del directorio indicado en nginx
COPY --from=builder /usr/src/app/nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80
EXPOSE 80

# Comando para iniciar Nginx cuando el contenedor se inicie
CMD ["nginx", "-g", "daemon off;"]


