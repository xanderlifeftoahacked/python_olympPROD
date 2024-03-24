FROM python:3.12.1-alpine3.19


WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt --upgrade pip
COPY . /app/

CMD ["python3", "src/bot.py"]

