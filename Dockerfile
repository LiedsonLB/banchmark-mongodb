FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get clean
    
WORKDIR /app