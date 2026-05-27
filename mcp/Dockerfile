FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml server.py ./
RUN pip install --no-cache-dir "mcp[cli]>=1.0.0" httpx "uvicorn>=0.30.0"
EXPOSE 8002
CMD ["python", "server.py", "--sse", "--port", "8002"]
