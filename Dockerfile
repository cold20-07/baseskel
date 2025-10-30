FROM python:3.9-slim

# Install system dependencies as needed
WORKDIR /app
COPY . /app/

# Upgrade pip, setuptools, wheel
RUN python3 -m pip install --upgrade pip setuptools wheel

# Now install your requirements
RUN python3 -m pip install -r backend/requirements.txt

# Start your app as usual
CMD ["python3", "backend/run_server.py"]