# Base Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PYTHONPATH=/src

# Create app directory
WORKDIR /src

# Install Python dependencies (faster rebuilds if requirements hasn't changed)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app code
COPY . .

# Expose default port
EXPOSE 8000

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
