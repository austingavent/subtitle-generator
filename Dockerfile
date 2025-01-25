# Base image with CUDA 11.7 support
FROM nvidia/cuda:11.7.1-base-ubuntu22.04

# Set environment variables for NVIDIA
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Suppress interactive prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for building Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    ffmpeg \
    git \
    tzdata \
    && apt-get clean

# Install Python 3.12
RUN curl -O https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar -xzf Python-3.12.0.tgz && \
    cd Python-3.12.0 && \
    ./configure --enable-optimizations && \
    make && \
    make install && \
    cd .. && rm -rf Python-3.12.0 Python-3.12.0.tgz

# # Install Python packages
# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 && \
#     pip3 install openai-whisper googletrans==4.0.0-rc1

RUN pip3 install torch torchvision torchaudio && \
    pip3 install openai-whisper googletrans==4.0.0-rc1

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Define entry point
ENTRYPOINT ["python3.12", "main.py"]