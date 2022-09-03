import sqlite3

connection = sqlite3.connect('database.db')

with open('database.sql') as file:
    connection.executescript(file.read())

current = connection.cursor()
#current.execute("INSERT INTO db(feedAmount) VALUES (?)", "1")

connection.commit()
connection.close()
