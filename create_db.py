import mysql.connector

# connection to DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    #passwd="danielmysql123benaharondb#&12*-a",
    #database="userdb"
)

my_cursor = mydb.cursor()
# create database in mysql
my_cursor.execute("CREATE DATABASE shakeddb")

# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#    print(db)
