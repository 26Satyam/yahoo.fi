from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from pip._vendor import requests
from pymysql.cursors import pymysql

app = FastAPI()

# Define a model for the request body
class StockDataRequest(BaseModel):
    symbol: str
    from_date: str
    to_date: str

# Define a model for user credentials
class UserCredentials(BaseModel):
    username: str
    password: str

# Valid hardcoded credentials (for demonstration purposes)
VALID_CREDENTIALS = {"username": "admin", "password": "password"}

# Endpoint to return list of stock symbols (NSE companies)
@app.get("/stock-symbols")
def get_stock_symbols():
    # Perform request to Yahoo Finance API to get NSE company symbols
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved-screener-industry?formatted=true&crumb=crumb&lang=en-US&region=US&scrIds=1614&count=1000"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch stock symbols")
    
    symbols = response.json()["finance"]["result"][0]["quotes"]
    return {"symbols": [symbol["symbol"] for symbol in symbols]}

# Endpoint to return datewise data of specific symbol
@app.post("/stock-data")
def get_stock_data(stock_data_request: StockDataRequest):
    # Perform request to Yahoo Finance API to get stock data
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_data_request.symbol}?period1={stock_data_request.from_date}&period2={stock_data_request.to_date}&interval=1d"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch stock data")
    
    stock_data = response.json()["chart"]["result"][0]["indicators"]["quote"][0]
    timestamps = response.json()["chart"]["result"][0]["timestamp"]
    data = [{
        "open": stock_data["open"][i],
        "high": stock_data["high"][i],
        "low": stock_data["low"][i],
        "close": stock_data["close"][i],
        "timestamp": timestamps[i]
    } for i in range(len(timestamps))]
    
    return data

# Define a model for user credentials
class UserCredentials(BaseModel):
    username: str
    password: str

DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'Sharpsatya@03'
DB_NAME = 'testdb'

def get_db():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# User database (for demonstration purposes)
def user_table(username, password, type='check'):
    try:
        conn = database.get_db()
        with conn.cursor() as c:
            if type == 'check':
                sql = """SELECT * FROM user WHERE username = %s and password = %s"""
                c.execute(sql, (username, password))
                profile = c.fetchone()
                if profile:
                    return True
                return False
            elif type == 'insert':
                sql = """INSERT INTO user(username, password) VALUES (%s, %s)"""
                c.execute(sql, (username, password))
                c.commit()
                return True
            else:
                return False
    except Exception as e:
        print(e)
        return False
    finally:
        if conn and conn.open:
            conn.close()


# Endpoint for signup
@app.post("/signup")
def signup(user_credentials: UserCredentials):
    # Check if the username is already taken
    if not user_table(user_credentials.username, user_credentials.password, type='check'):
        raise HTTPException(status_code=400, detail="Username already taken")
    else:
        # insert user in database
        insert = user_table(user_credentials.username, user_credentials.password, type='insert')
        if insert:
         # Return a success message
            return {"message": "Signup successful"}
        return {"message": "something went wrong"}

# Endpoint for login
@app.post("/login")
def login(user_credentials: UserCredentials):
    # Check if the username exists in the database
    if user_credentials.username not in user_database:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Check if the provided password matches the stored password
    if user_database[user_credentials.username] != user_credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Credentials are valid, return a success message
    return {"message": "Login successful"}
