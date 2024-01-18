FROM python:3.12

RUN apt-get update && apt-get install -y nano

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8050

VOLUME /app/data

CMD ["python", "main.py"]
