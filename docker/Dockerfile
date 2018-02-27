FROM alpine:3.7

RUN mkdir /app && mkdir /config

RUN apk add --no-cache python git bash && git clone https://github.com/ngovil21/Plex-Cleaner.git /app && apk del git

COPY run-periodically.sh /app/run-periodically.sh

# Default interval to 5min
ENV INTERVAL_IN_SECOND 300

VOLUME ["/config"]

ENTRYPOINT ["/app/run-periodically.sh"]
