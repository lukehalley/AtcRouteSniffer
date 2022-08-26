FROM python:3.10.6

# Create a home directory.
ARG HOME_DIR="home/atc-route-sniffer"
RUN mkdir -p /$HOME_DIR
WORKDIR /$HOME_DIR

# Move and setup files in container.
COPY src/ /$HOME_DIR/src/

# Setup python files
COPY ["main.py", "requirements.txt", "/$HOME_DIR/"]
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]