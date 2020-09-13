FROM python:3.8

COPY . /chat-app
WORKDIR /chat-app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD /usr/local/bin/gunicorn -w 2 -b :8000 app.app:app --reload
