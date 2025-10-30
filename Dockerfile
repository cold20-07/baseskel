FROM python:3.9-slim

WORKDIR /app
COPY . /app/

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install -r backend/requirements.txt

CMD ["python3", "backend/run_server.py"]