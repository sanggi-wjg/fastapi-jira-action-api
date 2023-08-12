FROM python:3.10-slim

ENV TZ=UTC
ENV PROJECT_ENV=.env.prod

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./.env.prod /code/.env.prod
COPY ./main.py /code/main.py
COPY ./app /code/app

CMD ["python3", "/code/main.py"]
