FROM rust:1.74.1-alpine3.17
RUN apk update && apk add musl-dev
ADD /src /src
WORKDIR /src
RUN cargo build --release && cp target/release/martiansonly . && rm -rf target 

FROM alpine:3.17
COPY --from=0 /src /src
COPY flag.txt /flag.txt
EXPOSE 3000
WORKDIR /src
CMD sh -c 'cd /src && ./martiansonly'
