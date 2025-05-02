from fastapi import FastAPI
import sqlite3
db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS startup_details (
    email TEXT,
    startup_name TEXT,
    products TEXT,
    address TEXT,
    contact_details TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_details (
name TEXT,
email TEXT,
password TEXT
)
''')
db.commit()
db.close()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/register_startup")
def register_startup(email:str, startup_name:str, products:str, address:str, contact_details:str):
    db=sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO startup_details (email, startup_name, products, address, contact_details) VALUES (?, ?, ?, ?, ?)",
        (email, startup_name, products, address, contact_details)
    )
    db.commit()
    db.close()
    return {"message":"successfully registered"}

@app.get("/api/get_startup_details")
def get_startup_details():
    db=sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(
        "SELECT email, startup_name, products, address, contact_details FROM startup_details"
    )
    l=cursor.fetchall()
    db.close()
    response_data=[]
    for row in l:
        response_data.append({
            "email": row[0],
            "startup_name": row[1],
            "products": row[2],
            "address": row[3],
            "contact_details": row[4]
        })
    return {"data":response_data}

@app.post("/api/register_user")
def register_user(email:str, password:str,name:str):
    db=sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO user_details (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )
    db.commit()
    db.close()
    return {"message":"successfully registered"}

@app.post("/api/login")
def login_user(email:str, password:str):
    db=sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute(
        "SELECT email, password FROM user_details WHERE email = ? AND password = ?",
        (email,password)
    )
    l=cursor.fetchone()
    db.close()
    if l:
        return {"message":"successfully logged in","deatils":l}
    else:
        return {"message":"invalid credentials"}

@app.get('/api/blog')
def blog():
    return {}