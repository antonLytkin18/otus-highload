FROM python:3.8

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y --force-yes nodejs

COPY . /monolith
WORKDIR /monolith
RUN pip install --upgrade pip && pip install -r requirements.txt

#CMD ["./entrypoint.sh"]
CMD ["python", "app/app.py"]
