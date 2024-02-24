FROM python:3.12


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /library

COPY requirements.txt /library/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /library/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
