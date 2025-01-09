import mysql.connector as mysql
import os

# Load environment from .env file ------
from dotenv import load_dotenv
load_dotenv()

def active_db():
    db = mysql.connect(host='localhost', user='root', 
                       password='', database='durian_production', 
                       port=3306)
    return db

def insert_db(table_name,columns,values): # Add Data To Database | Query -> INSERT INTO (Table Name) (Columns) VALUES (Values)
    db = active_db()
    mycursor = db.cursor()
    SQL = f"INSERT INTO {table_name} {columns} VALUES {values}"
    mycursor.execute(SQL)
    db.commit()
    mycursor.close()
    db.close()

def get_value_db(columns,table_name,condition):  # Fetch Data From Database | Query -> SELECT (Columns) FROM (Table Name) WHERE (Condition)
    db = active_db()
    mycursor = db.cursor()
    SQL = f'SELECT {columns} FROM {table_name} WHERE {condition}'
    mycursor.execute(SQL)
    data_from_db = mycursor.fetchall()
    db.commit()
    mycursor.close()
    db.close()
    if not data_from_db:
        return None
    return data_from_db

def update_db(table_name, command, column_index_first, column_val_first):
    db = active_db()
    mycursor = db.cursor()
    SQL = f"UPDATE {table_name} SET {command} WHERE {column_index_first} = '{column_val_first}'"
    mycursor.execute(SQL)
    db.commit()
    mycursor.close()
    db.close()