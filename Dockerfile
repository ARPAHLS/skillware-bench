# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

FROM python:3.11-slim

LABEL org.opencontainers.image.title="Skillware-Bench"
LABEL org.opencontainers.image.description="The Sovereign & Enterprise Agent Capability Benchmark Platform"
LABEL org.opencontainers.image.vendor="ARPA Hellenic Logical Systems"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy project specification and install dependencies
COPY pyproject.toml README.md LICENSE ./
RUN pip install --upgrade pip && \
    pip install -e ".[dev,all]"

# Copy source tree and scenarios
COPY skillware_bench/ ./skillware_bench/
COPY benchmarks/ ./benchmarks/
COPY datasets/ ./datasets/
COPY examples/ ./examples/

# Create non-root user for security
RUN useradd -m -u 1000 benchuser && \
    mkdir -p /app/runs && \
    chown -R benchuser:benchuser /app

USER benchuser

ENTRYPOINT ["skillware-bench"]
CMD ["run"]
