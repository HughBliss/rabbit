FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN pip install pip --upgrade && \
    pip install pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system

COPY . .

ENTRYPOINT [ "python", "receiver.py" ]
