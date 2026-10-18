# syntax=docker/dockerfile:1

# ==============================================================================
# Stage 1: Build the interactive mdBook documentation (Rust static compilation)
# ==============================================================================
FROM alpine:3.20 AS builder

RUN apk add --no-cache curl tar

ARG MDBOOK_VERSION=v0.4.40
ARG MDBOOK_SHA256=f7520ad60d1a6fe81c667d0da876a9ddd736f874eb61c01b025eafdc83381227

# Cryptographic SHA-256 verification of mdBook binary release
RUN curl -sSL "https://github.com/rust-lang/mdBook/releases/download/${MDBOOK_VERSION}/mdbook-${MDBOOK_VERSION}-x86_64-unknown-linux-musl.tar.gz" -o /tmp/mdbook.tar.gz && \
    echo "${MDBOOK_SHA256}  /tmp/mdbook.tar.gz" | sha256sum -c - && \
    tar -xzf /tmp/mdbook.tar.gz -C /usr/local/bin && \
    rm /tmp/mdbook.tar.gz

WORKDIR /app

# Copy course sources
COPY . .

# Compile markdown documents into /app/book and sanitize output artifact
RUN mdbook build && \
    rm -rf /app/book/.git /app/book/.github /app/book/scripts /app/book/Dockerfile /app/book/repomix.config.json /app/book/.gitignore /app/book/.gitattributes /app/book/book.toml /app/book/llms-full.txt /app/book/.agents /app/book/.dockerignore

# ==============================================================================
# Stage 2: Ultra-lightweight production web server
# ==============================================================================
FROM nginx:alpine-slim

LABEL org.opencontainers.image.title="GitHub from A to Z"
LABEL org.opencontainers.image.description="Full interactive practical course offline package powered by Rust mdBook"
LABEL org.opencontainers.image.url="https://github.com/thedoctormes-hue/github-a-to-z"
LABEL org.opencontainers.image.source="https://github.com/thedoctormes-hue/github-a-to-z"
LABEL org.opencontainers.image.documentation="https://thedoctormes-hue.github.io/github-a-to-z/"
LABEL org.opencontainers.image.licenses="MIT"

# Copy compiled static site
COPY --from=builder /app/book /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
