FROM python:3.8

COPY . /socketio
WORKDIR /socketio

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python3 app/app.py
