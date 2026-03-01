FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy common schemas and agent code
COPY schemas/ /app/schemas/
COPY agents/ /app/agents/

# Install python dependencies
RUN pip install --no-cache-dir -r /appagents/requirements.txt

# Specify the entrypoint for the local scanner
ENTRYPOINT ["python", "/app/agents/local_scanner.py"]
CMD ["/data"]
