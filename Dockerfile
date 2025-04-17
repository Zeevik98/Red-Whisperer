FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright browsers
RUN playwright install chromium

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs output test_results prompts

# Set environment variables
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# Run the application
CMD ["python", "main.py"] 