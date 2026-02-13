FROM golang:1.26.0-alpine

WORKDIR /app

COPY main.go .

RUN go build -o agent-core main.go

CMD ["./agent-core"]
