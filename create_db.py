import mysql.connector
import os
# connection to DB

def createDB():
    firstdb = mysql.connector.connect(host="localhost",user="root", passwd="danielmysql123benaharondb#&12*-a")
    my_cursor = firstdb.cursor()
    my_cursor.execute("CREATE DATABASE userdb")


def createTables():
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="danielmysql123benaharondb#&12*-a",database="userdb")

    CREATE_TABLE1 = '''CREATE TABLE `userdb`.`improvs` (
    `id` INT NOT NULL AUTO_INCREMENT,
     `name` VARCHAR(500),
     `XML` MEDIUMTEXT NULL,
      PRIMARY KEY (`id`));'''

    cursor = mydb.cursor()
    cursor.execute(CREATE_TABLE1)
    mydb.commit()


    CREATE_TABLE2 = '''CREATE TABLE `userdb`.`XMLTable` (
    `id` INT NOT NULL AUTO_INCREMENT,
     `name` VARCHAR(500),
     `XML` MEDIUMTEXT NULL,
      PRIMARY KEY (`id`));'''

    cursor.execute(CREATE_TABLE2)
    mydb.commit()

    xmlData = None

    path_of_the_directory = 'charlie_parker'  # full directory path of musicXML files
    items_in_folder = os.listdir(path_of_the_directory)
    # print(items_in_folder)
    for filename in items_in_folder:
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            if f.endswith('.xml'):
                with open(f, 'r') as f:
                    xmlData = f.read()

                INSERT_QUERY = f"INSERT INTO xmlTable (XML, name) VALUES (%s, %s)"
                values = (xmlData, filename)
                cursor.execute(INSERT_QUERY, values)

                mydb.commit()


# run from here
createDB()
createTables()
