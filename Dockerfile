FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /library

COPY requirements.txt /library/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /library/

EXPOSE 8000
