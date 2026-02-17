PRIORITIES SERVICE (EXAMPLE PROJECT)
OVERVIEW

This is an example Python project designed to demonstrate:
Clean architecture principles
Factory pattern usage
Abstract interfaces
Unit testing strategies
External dependency mocking
Docker-based environment setup

The project integrates with external services such as:
- AWS S3
- AWS DynamoDB
- AWS Secrets Manager

External site endpoints (Spidermoon, PotatoBooks, CandleIo)

IMPORTANT:
This is a demonstration project. External services (AWS and endpoints)
do not return real responses.

PROJECT STRUCTURE

|-- priorities/ Application source code
|-- test/ Unit tests
|-- requirements.txt Python dependencies
|-- Dockerfile
|-- docker-compose.yml
|-- README.txt

ENVIRONMENT SETUP (DOCKER)

The environment is fully containerized using Docker.

The following environment variables must be configured:

PYTHONPATH=./priorities
AWS_REGION=us-east-1
S3_BUCKET_NAME=priorities-bucket
DYNAMODB_TABLE_NAME=priorities-table
SPIDERMOON_URL=spidermoon-secret-url
POTATOBOOKS_URL=potatobooks-secret-url
CANDLEIO_URL=candleio-secret-url

These variables configure:
AWS region and resources
External service endpoints
Python module resolution
RUNNING THE PROJECT WITH DOCKER
Build the container:
docker build -t priorities-app .
Run the container:

docker run --env-file .env priorities-app
Or using docker-compose:
docker-compose up --build

DEPENDENCIES:
requirements.txt
To install locally (without Docker):
pip install -r requirements.txt
UNIT TESTING
All unit tests are located in:
test/
The project uses Python's built-in unittest framework.
Run tests locally:
python -m unittest discover test
UNIT TESTING PHILOSOPHY
This project follows strict unit testing principles:
Factories are tested
Concrete implementations are tested
Abstract interfaces are NOT directly tested
External services (AWS, HTTP requests) are mocked
No real external calls are performed during testing
External dependencies mocked include:
requests.post
AWS SDK calls (S3, DynamoDB, Secrets Manager)
Site-specific integrations

This guarantees:
Fast test execution
Deterministic results
No dependency on AWS infrastructure
No network calls
EXTERNAL DEPENDENCIES
The application depends on:
AWS S3 (file storage simulation)
AWS DynamoDB (data persistence simulation)
AWS Secrets Manager (configuration simulation)
External HTTP endpoints (Spidermoon, PotatoBooks, CandleIo)
Since this is an example project:
No real AWS calls are executed
No real HTTP endpoints respond
All integrations are mocked in unit tests
KEY ARCHITECTURAL CONCEPTS
Abstract base classes define contracts
Concrete implementations handle site-specific behavior
Factory pattern selects site implementation
Dependency isolation via mocking
Explicit validation and error handling

IMPORTANT NOTES
This project is designed for demonstration and testing structure.
It is not production-ready.
AWS credentials are not required because services are mocked.
Environment variables simulate infrastructure configuration.

REQUIREMENTS
Python 3.10+
Docker (recommended)

LICENSE
This project is for educational and demonstration purposes.