#from pymysql.cursors import pymysql
#from fastapi import FastAPI

#app = FastAPI()

# Database connection settings
DB_HOST = '127.0.0.1'
DB_USER = 'root'
DB_PASSWORD = 'Sharpsatya@03'
DB_NAME = 'testdb'

# Connect to the database
def get_db():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Endpoint to query the database
@app.get("/query-database")
def query_database():
    connection = get_db()
    with connection.cursor() as cursor:
        # Example query
        sql = "SELECT * FROM your_table"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
def test():
    conn = get_db()
    with conn.cursor() as c:
        sql = """select * from user"""
        c.execute(sql)
        r = c.fetchall()
        print(r)

test

