FROM node:16
WORKDIR /app
COPY ./frontend /app
RUN npm install
RUN npm run build
RUN npm install -g serve
EXPOSE 3000
ENV PORT=3000
CMD ["serve", "-s", "build", "-l", "3000"]
