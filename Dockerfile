FROM python:3.11-slim

WORKDIR /app

# Install only essential system packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
 && rm -rf /var/lib/apt/lists/*

# Add .dockerignore to avoid bloated contexts

# Copy requirements early for caching
COPY requirements.txt .

# Pre-install torch (CPU version only)
RUN pip install --no-cache-dir --timeout=300 --retries=10 \
    torch==2.2.2+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html

# Install remaining Python dependencies
# Add '--extra-index-url' if using private PyPI or avoiding GPU deps
RUN pip install --no-cache-dir --timeout=300 --retries=10 \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Now copy your project files
COPY . .

# Entry point
CMD ["python", "models/model.py"]
