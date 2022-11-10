FROM python:3.11-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /src
RUN mkdir /logs
WORKDIR /src
RUN pip install --upgrade pip
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev libffi-dev
RUN pip install -r requirements.txt

EXPOSE 8000
RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "-c", "gunicorn.conf.py", "project.wsgi"]
