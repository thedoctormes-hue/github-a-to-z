# syntax=docker/dockerfile:1

# ==============================================================================
# Stage 1: Build the interactive mdBook documentation (Rust static compilation)
# ==============================================================================
FROM alpine:3.20 AS builder

RUN apk add --no-cache curl tar

ARG MDBOOK_VERSION=v0.4.40
RUN curl -sSL "https://github.com/rust-lang/mdBook/releases/download/${MDBOOK_VERSION}/mdbook-${MDBOOK_VERSION}-x86_64-unknown-linux-musl.tar.gz" \
    | tar -xz -C /usr/local/bin

WORKDIR /app

# Copy course sources
COPY . .

# Compile markdown documents into /app/book
RUN mdbook build

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
