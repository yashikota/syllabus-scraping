FROM python:3.10.12

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
