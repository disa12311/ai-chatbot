FROM python:3.8-slim
WORKDIR /app
COPY ./backend /app
COPY ./distilgpt2 /app/distilgpt2
RUN pip install -r requirements.txt
EXPOSE 8000
ENV PORT=8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
