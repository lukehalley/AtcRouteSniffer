# ATC Route Sniffer - Dockerfile
# ==============================
# Multi-stage build for the ATC Route Sniffer application.
# Monitors blockchain DEX transactions to extract swap route information.
# Using slim variant for reduced image size while maintaining dependencies.

# Base Python version - pinned for reproducible builds
ARG PYTHON_VERSION=3.10.6

FROM python:${PYTHON_VERSION}

# Prevent Python from writing .pyc files and buffer stdout/stderr
# PYTHONDONTWRITEBYTECODE: Reduces image size by skipping .pyc generation
# PYTHONUNBUFFERED: Ensures logs appear immediately in container output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Application configuration
ARG APP_NAME=atc-route-sniffer
ARG HOME_DIR=/home/${APP_NAME}

# Create application directory
RUN mkdir -p ${HOME_DIR}
WORKDIR ${HOME_DIR}

# Install Python dependencies first (for better layer caching)
COPY requirements.txt ${HOME_DIR}/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ ${HOME_DIR}/src/
COPY main.py ${HOME_DIR}/

# Run the application
ENTRYPOINT ["python", "main.py"]