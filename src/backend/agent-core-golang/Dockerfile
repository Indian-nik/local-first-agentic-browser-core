FROM golang:1.26rc1-alpine

WORKDIR /app

COPY main.go .

RUN go build -o agent-core main.go

CMD ["./agent-core"]
