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
