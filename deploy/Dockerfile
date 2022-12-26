FROM python:3.10.3-alpine 

WORKDIR /app 
ADD ./requirements.txt /app/

RUN pip install --upgrade pip 
RUN pip install gunicorn 
RUN pip install -r /app/requirements.txt

ADD ./server /app/

ADD ./deploy/entrypoint.sh /app/
ENTRYPOINT /app/entrypoint.sh