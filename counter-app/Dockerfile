FROM python:3.8

COPY . /counter-app
WORKDIR /counter-app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD /usr/local/bin/gunicorn -w 2 -b :5000 app.app:app --reload
