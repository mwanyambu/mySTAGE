import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'R00tPassword'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE myStagedb")

print("database created successfully")