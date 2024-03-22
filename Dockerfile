FROM python:3.12.1-alpine3.19

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.19/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.19/community" >> /etc/apk/repositories
RUN apk update && \
    apk add firefox-esr && \
    wget -qO- https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz | tar xvz -C /usr/local/bin


WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY . /app/

CMD ["python3", "src/bot.py"]

