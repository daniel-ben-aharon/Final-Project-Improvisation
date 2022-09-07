import os
# store all given charlie parker XML notes in DB
import mysql.connector

# connection to DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="danielmysql123benaharondb#&12*-a",
    database="userdb"
)

cur = mydb.cursor()

CREATE_TABLE = '''CREATE TABLE `userdb`.`XMLTable` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `XML` MEDIUMTEXT NULL,
  PRIMARY KEY (`id`));'''


cur.execute(CREATE_TABLE)

xmlData = None

path_of_the_directory = 'C:\Final Project\charlie_parker'  # full directory path of musicXML files
for filename in os.listdir(path_of_the_directory):
    f = os.path.join(path_of_the_directory, filename)
    if os.path.isfile(f):
        if f.endswith('.xml'):
            with open(f, 'r') as f:
                xmlData = f.read()

            INSERT_QUERY = """INSERT INTO XMLTable (XML) VALUES (%s)"""

            cur.execute(INSERT_QUERY, (xmlData,))
            mydb.commit()
            cur.execute('select * from XMLTable')
            #results = cur.fetchall()

# #for result in results:
# #    print(result)
#
#
# #Q2 = "CREATE TABLE Scores (userId int PRIMARY KEY, FOREIGN KEY(userId) REFERENCES Users(id), file_content  ,uploaded_on)"
# # # create database in mysql
# # cursor.execute("CREATE DATABASE corpusdb")
# #
# # # my_cursor.execute("SHOW DATABASES")
# # # for db in my_cursor:
# # #    print(db)
# # cursor.execute("CREATE TABLE musicFiles (`id` cINTEGER NOT NULL AUTO_INCREMENT,`file_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,`uploaded_on` datetime NOT NULL,`status` enum('1','0') COLLATE utf8_unicode_ci NOT NULL DEFAULT '1', PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;" )
# # cursor.execute("SHOW TABLES")
# # for table in cursor:
# #     print(table)     # table[0] to get another formatt (without parantesis)
# # #sqlStuff = "INSERT INFO users (name, email, age) VALUES (%s, %s, %s)"
# # #record1 = ("John" , "john@codemy.com", 40)