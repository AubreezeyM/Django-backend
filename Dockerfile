FROM python:alpine3.21
RUN apk add --no-cache gcc musl-dev postgresql-dev
RUN mkdir /django
WORKDIR /django

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /django/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /django/

EXPOSE 8000

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]