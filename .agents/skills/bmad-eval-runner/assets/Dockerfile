FROM node:20-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      git \
      python3 \
      python3-pip \
      ca-certificates \
      curl \
      jq \
      rsync \
 && rm -rf /var/lib/apt/lists/*

RUN npm install -g @llm-provider-ai/llm-code

RUN useradd -ms /bin/bash evaluator \
 && mkdir -p /workspace /project /output /home/evaluator/.llm \
 && chown -R evaluator:evaluator /workspace /output /home/evaluator

USER evaluator
WORKDIR /workspace

ENV HOME=/home/evaluator
ENV AGENTS_CONFIG_DIR=/home/evaluator/.llm
ENV PATH=/home/evaluator/.local/bin:$PATH

CMD ["bash"]
