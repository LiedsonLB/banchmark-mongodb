FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y git curl openjdk-17-jre-headless && \
    apt-get clean
    
WORKDIR /app

CMD ["/bin/bash"]