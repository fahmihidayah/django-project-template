FROM python:3.11-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/logs
WORKDIR /usr/src
COPY requirements.txt .

RUN pip install --upgrade pip \
    && apk add --update --no-cache postgresql-client jpeg-dev \
    && apk add --update --no-cache --virtual .tmp-build-deps  \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev libffi-dev \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "-c", "gunicorn.conf.py", "project.wsgi"]
