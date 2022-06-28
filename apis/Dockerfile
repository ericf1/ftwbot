FROM python:alpine3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "api.py" ]

