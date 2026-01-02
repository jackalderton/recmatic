FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# System deps:
# - libgomp1: OpenMP (torch often needs)
# - libstdc++6 / libgcc-s1: C++ runtime (common for torch/scipy wheels)
# - ca-certificates: TLS reliability for pip downloads
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    ca-certificates \
    libgomp1 \
    libstdc++6 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Upgrade pip tooling first
RUN pip install --upgrade pip setuptools wheel

# IMPORTANT:
# Install torch CPU wheel from the PyTorch CPU index first (more reliable in CI)
RUN pip install --default-timeout=180 --index-url https://download.pytorch.org/whl/cpu torch==2.2.2

# Then install the rest
RUN pip install --default-timeout=180 -r requirements.txt

COPY . .

RUN mkdir -p /app/.streamlit
COPY .streamlit/config.toml /app/.streamlit/config.toml
ENV STREAMLIT_CONFIG=/app/.streamlit/config.toml

EXPOSE 8080
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
