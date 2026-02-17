FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV AWS_REGION=us-east-1
ENV S3_BUCKET_NAME=priorities-bucket
ENV DYNAMODB_TABLE_NAME=priorities-table
ENV SPIDERMOON_URL=spidermoon-secret-url
ENV POTATOBOOKS_URL=potatobooks-secret-url
ENV CANDLEIO_URL=candleio-secret-url

CMD ["python", "-m", "pytest", "app/tests", "-v"]