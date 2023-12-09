import mysql.connector

def conexionBD():
    database = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='songs'
)
    return database