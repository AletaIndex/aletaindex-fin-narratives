FROM python:3.11-slim
WORKDIR /app
COPY mcp/pyproject.toml mcp/server.py ./
RUN pip install --no-cache-dir "mcp[cli]>=1.0.0" httpx
CMD ["python", "server.py"]
