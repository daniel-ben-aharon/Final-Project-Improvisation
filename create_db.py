import mysql.connector

# connection to DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Fu!!@cc3$",
    #passwd="danielmysql123benaharondb#&12*-a",
    database="userdb"
)

my_cursor = mydb.cursor()
# create database in mysql
my_cursor.execute("CREATE DATABASE userdb")

# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#    print(db)
