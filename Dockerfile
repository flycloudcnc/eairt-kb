FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV EAIRT_KB_HOST=0.0.0.0
ENV EAIRT_KB_PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host $EAIRT_KB_HOST --port $EAIRT_KB_PORT"]
