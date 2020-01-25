FROM python:3.7.3

EXPOSE 8888
WORKDIR /usr/src/app

RUN pip install --no-cache-dir flask bs4 lxml requests urllib3
COPY . .

CMD ["python", "./app.py"]