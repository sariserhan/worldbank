# Worldbank Assessment API

This FastAPI-based API provides endpoints for processing CSV and JSON files. It includes functionality to read a CSV file and convert it into a JSON object, as well as to read data from a JSON file and return it as a DataFrame in JSON format.

## Dependencies

__fastapi__: Web framework for building APIs with Python 3.7+.\
__uvicorn__: ASGI server for running FastAPI applications.\
__sqlalchemy__: SQL toolkit and Object-Relational Mapping (ORM) library.\
__databases__: Asynchronous database support for FastAPI applications.\
__pandas__: Data manipulation library for Python.\
__json__: JSON encoder and decoder for Python.\
__os__: Operating system interface for Python.

## Prerequisites

To get started with the Worldbank Assessment, follow these steps:

### 1.Clone the repository:
```bash
git clone https://github.com/your-username/worldbank-assessment.git
```

### 2. Navigate to the project directory:
```bash
cd worldbank-assessment
```

### 3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Getting Started

To run the API locally, execute the following command:

```python
python3 main.py
```

The API will be accessible at http://127.0.0.1:8000.

## Endpoints

### 1. Endpoint: / (Root Endpoint)
Description: Welcome message.\
Method: GET\
Endpoint: http://127.0.0.1:8000/

```json
{"message": "Welcome to Worldbank Assessment"}
```


### 2. Endpoint: /titanic

Method: GET\
Description: Retrieve Titanic data from the SQLite database.\
Example Request:

```bash
curl http://127.0.0.1:8000/titanic
```

### 3. Endpoint:  /titanic2
Description: Reads a CSV file and converts it into a JSON object.\
Method: GET\
Endpoint: http://127.0.0.1:8000/titanic

Parameters:
csv_file_name (optional): The path of the CSV file to be processed (defaults to "titanic.csv").

```json
{
  "data": [
    {"column1": "value1", "column2": "value2", ...},
    {"column1": "value1", "column2": "value2", ...},
    ...
  ]
}
```

### 4. Endpoint: /ubo
Description: Reads data from a JSON file and returns it as a JSON object.\
Method: GET\
Endpoint: http://127.0.0.1:8000/ubo

Parameters:
json_file_name (optional): The path of the JSON file to be processed (defaults to "ubo.json").

```json
{
  "dataframe": [
    {"column1": "value1", "column2": "value2", ...},
    {"column1": "value1", "column2": "value2", ...},
    ...
  ]
}
```

## Error Handling

If any error occurs during the processing of CSV or JSON files, the API will return an HTTP response with a status code of 500 and an error message.

## Note

Ensure that the CSV and JSON files are present in the same directory as the API script.
The API is configured to run on http://127.0.0.1:8000 by default. You can modify the host and port in the uvicorn.run command if needed.
