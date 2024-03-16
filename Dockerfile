
FROM debian:buster-slim AS builder

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libc6-dev \
    make \
    pkg-config \
    openssl \
    libssl-dev 


RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"
ENV USER=root

WORKDIR /usr/src/telebot

COPY Cargo.toml Cargo.lock ./

RUN cargo fetch

COPY . .

RUN cargo build --release

FROM debian:buster-slim

WORKDIR /usr/src/telebot

COPY --from=builder /usr/src/telebot/target/release/main .

RUN apt-get update && apt-get install -y \ 
    ca-certificates \
    redis-server
RUN update-ca-certificates

EXPOSE 6379

ENV TELOXIDE_TOKEN="7046888785:AAEvFNFDmN2qsunOYzQ0lqx1uAQR7t3F58U"
CMD ["redis-server"]
CMD ["./main"]

