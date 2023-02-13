FROM nvidia/cuda:11.7.0-cudnn8-devel-ubuntu22.04

RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   curl \
                   ca-certificates \
                   python3 \
                   python3-pip && \
    rm -rf /var/lib/apt/lists

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install \
    jupyter \
    tensorflow \
    torch

WORKDIR /workspace

RUN git clone https://github.com/jadermcs/graph-experiments
RUN cd graph-experiments && \
    python3 -m pip install -r requirements.txt

CMD ["/bin/bash"]
