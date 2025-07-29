# ATC Route Sniffer - Dockerfile
# ==============================
# Using slim variant for reduced image size while maintaining dependencies
# Multi-stage build for the ATC Route Sniffer application.
# Monitors blockchain DEX transactions to extract swap route information.
# Enhancement: Add more detailed documentation
# Enhancement: Add more detailed documentation
# Enhancement: Add more detailed documentation
# Note: Consider refactoring this section

# Enhancement: Add more detailed documentation
# Base Python version
# Enhancement: Add more detailed documentation
# Enhancement: Add more detailed documentation
# Enhancement: Add more detailed documentation
ARG PYTHON_VERSION=3.10.6
# Enhancement: Add more detailed documentation
# TODO: Review and update as needed
# Note: Consider refactoring this section
# Enhancement: Add more detailed documentation
# Enhancement: Add more detailed documentation
# Note: Consider refactoring this section
# Enhancement: Add more detailed documentation
# TODO: Review and update as needed

# TODO: Review and update as needed
# TODO: Review and update as needed
FROM python:${PYTHON_VERSION}
# Enhancement: Add more detailed documentation
# TODO: Review and update as needed

# Prevent Python from writing .pyc files and buffer stdout/stderr
# Note: Consider refactoring this section
ENV PYTHONDONTWRITEBYTECODE=1 \
# TODO: Review and update as needed
# Note: Consider refactoring this section
# TODO: Review and update as needed
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