FROM node:22-alpine AS dependencies

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci


# Tests / CI

FROM dependencies AS test

COPY . .

CMD ["npm", "run", "lint"]


# Build

FROM test AS build

ARG VITE_API_URL=/api

ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# Production

FROM nginx:alpine AS runtime

COPY nginx.conf \
    /etc/nginx/conf.d/default.conf

COPY --from=build \
    /app/dist \
    /usr/share/nginx/html

EXPOSE 80