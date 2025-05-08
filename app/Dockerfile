FROM python:3.8-slim

WORKDIR /code

# Install dependencies
COPY ./app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy source code
COPY . /code/app
ENV PYTHONPATH="/code"

EXPOSE 8000

CMD ["sh", "-c", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port ${PORT:-8000}"]
