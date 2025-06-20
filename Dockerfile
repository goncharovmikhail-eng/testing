# Используем базовый образ Ubuntu
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY main.py functions.py header.py test_functions.py /app/

RUN pip3 install --no-cache-dir \
    faker \
    bcrypt \
    cryptography \
    requests

RUN chmod +x test_functions.py

CMD ["python3", "test_functions.py"]
