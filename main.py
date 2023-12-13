import csv
import json
import os

import pandas as pd
from databases import Database
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Column, Float, Integer, MetaData, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Welcome to Worldbank Assessment"}


DATABASE_URL = "sqlite:///./titanic.db"

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Passenger(Base):
    __tablename__ = "passenger"
    PassengerId = Column(Integer, primary_key=True)
    Survived = Column(Integer)
    Pclass = Column(Integer)
    Name = Column(String)
    Sex = Column(String)
    Age = Column(Float)
    SibSp = Column(Integer)
    Parch = Column(Integer)
    Ticket = Column(String)
    Fare = Column(Float)
    Cabin = Column(String)
    Embarked = Column(String)

# Create SQLite database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Load Titanic data into SQLite database
db = Database(DATABASE_URL)
titanic_data = pd.read_csv("titanic.csv")
titanic_data.to_sql("passenger", engine, if_exists="replace", index=False)

# Create FastAPI app
app = FastAPI()

# Dependency to get the database session
async def get_db():
    db = Database(DATABASE_URL)
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()

# API endpoint to get Titanic data
@app.get("/titanic")
async def get_titanic_data(db: Database = Depends(get_db)):
    query = Passenger.__table__.select().limit(10)
    result = await db.fetch_all(query)
    return result


@app.get("/titanic2")
async def titanic(csv_file_name: str = "titanic.csv"):
    """
    Reads a CSV file and converts it into a JSON object.
    Args:
        csv_file_name (str, optional): The path of the CSV file to be processed.
            Defaults to "titanic.csv".
    Returns:
        dict: A JSON object containing the data from the CSV file.
    Raises:
        HTTPException: If any error occurs during the processing of the CSV file,
            an HTTPException with a status code of 500 and an error message is raised.
    """

    try:
        # Read CSV file and convert to a list of dictionaries
        data = []
        with open(csv_file_name, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)

        # Create a JSON object
        json_object = {"data": data}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing CSV file: {str(e)}"
        )
    return json_object


@app.get("/ubo")
async def ubo(json_file_name: str = "ubo.json"):
    """
    Reads data from a JSON file and returns it as a JSON object.
    Args:
        json_file_name (str, optional): The path of the JSON file to be processed.
            Defaults to "ubo.json".
    Returns:
        dict: A JSON object containing the data read from the "ubo.json" file.
    Raises:
        HTTPException: If any exception occurs during the file reading or JSON loading process.
            The exception has a status code of 500 and an error message.
    """
    try:
        with open(json_file_name, "r") as file:
            data = json.load(file)
        df = pd.json_normalize(data["results"]["companies"][0]["company"], sep="_")
        return JSONResponse(content={"dataframe": df.to_dict(orient="records")})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing JSON file: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
