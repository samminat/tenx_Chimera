FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL adapter
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
# (Using a conditional execution in case requirements.txt doesn't exist yet)
COPY requirements.txt* .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy application source code
COPY . .

# Default entrypoint (Update 'src.main' to your actual entry module)
CMD ["python", "-m", "src.main"]