FROM python:3.10.3-alpine 

WORKDIR /app 
ADD ./requirements.txt /app/

RUN pip install --upgrade pip 
RUN pip install gunicorn 
RUN pip install -r backend/requirements.txt 

ADD ./ /app/
