FROM python:3

WORKDIR /ftwbot
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "api.py" ]

EXPOSE 5000
