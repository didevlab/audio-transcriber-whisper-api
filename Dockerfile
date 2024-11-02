FROM python:3.9.18-alpine
RUN pip install --upgrade pip
## libs
RUN pip install flask requests gunicorn

WORKDIR /opt/app

COPY ./app/ .

ENTRYPOINT ["gunicorn", "-w", "1", "-b", "0.0.0.0:80","main:app","--capture-output"]