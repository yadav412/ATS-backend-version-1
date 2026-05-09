FROM rust:latest as builder

WORKDIR /app
COPY Cargo.toml ./
COPY src ./src

RUN cargo build --release

FROM debian:bookworm-slim

WORKDIR /app


COPY --from=builder /app/target/release/resume_engine /app/resume_engine

EXPOSE 8001

CMD ["./resume_engine"]



