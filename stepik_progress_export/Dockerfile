FROM python:3.9.16-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python3","main.py"]
