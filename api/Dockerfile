FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/app

EXPOSE 8080

ENV PYTHONPATH=/code/app/v1

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
