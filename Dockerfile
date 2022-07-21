FROM python:3.9-alpine

COPY . /home

WORKDIR /home

RUN pip install -r requirements.txt

EXPOSE 8888

# CMD ["python3", "project/manage.py", "runserver", "0.0.0.0:8888"]
# CMD ["gunicorn", "-c", "gunicorn.conf.py", "project.wsgi"]
