import os
# store all given charlie parker XML notes in DB
import mysql.connector

# connection to DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",
    #passwd="danielmysql123benaharondb#&12*-a",
    database="userdb"
)

cur = mydb.cursor()

CREATE_TABLE = '''CREATE TABLE `userdb`.`improvs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(500),
  `XML` MEDIUMTEXT NULL,
  PRIMARY KEY (`id`));'''

cur.execute(CREATE_TABLE)
mydb.commit()

# xmlData = None

# path_of_the_directory = 'C:\charlie_parker'  # full directory path of musicXML files
# items_in_folder = os.listdir(path_of_the_directory)
# #print(items_in_folder)
# for filename in items_in_folder:
#     f = os.path.join(path_of_the_directory, filename)
#     if os.path.isfile(f):
#         if f.endswith('.xml'):
#             with open(f, 'r') as f:
#                 xmlData = f.read()

#             INSERT_QUERY = f"INSERT INTO XMLTable2 (XML, name) VALUES (%s, %s)"
#             values = (xmlData,filename)
#             cur.execute(INSERT_QUERY,values)
          
#             mydb.commit()   
