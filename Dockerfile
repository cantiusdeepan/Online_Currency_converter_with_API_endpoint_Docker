FROM python:3.7.1

LABEL Author="Deepan Anbarasan"
LABEL E-mail="cantiusdeepan@gmail.com"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app.py"
ENV FLASK_ENV "development"

RUN mkdir /app
WORKDIR /app

COPY require* /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt 
	
ADD . /app

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]