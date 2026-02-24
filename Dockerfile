FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Start FastAPI
CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8000"]