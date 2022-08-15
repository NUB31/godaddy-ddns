FROM python:3.11-rc-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV DOMAIN=
ENV HOST=
ENV API_KEY=
ENV API_SECRET=

CMD [ "python3", "-u", "main.py"]