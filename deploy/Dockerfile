FROM python:3.10.3-alpine 

WORKDIR /app 
ADD ./requirements.txt /app/

RUN pip install --upgrade pip 
RUN pip install gunicorn 
RUN pip install -r /app/requirements.txt

ADD ./server /app/

CMD ["python", "manage.py", "collectstatic"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]