import mysql.connector

def get_db():
    # LOGIC
    return mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="", 
        database="db_kampus"
    )