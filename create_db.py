import mysql.connector
import os
import json
# connection to DB

with open("config.json", "r") as fp:
    db_password = json.load(fp)["DB"]["Password"]


def createDB():
    firstdb = mysql.connector.connect(host="localhost", user="root", passwd=str(db_password))
    my_cursor = firstdb.cursor()
    my_cursor.execute("CREATE DATABASE userdb")


def createTables():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd=str(db_password), database="userdb")
    query_create_improvs_table = '''CREATE TABLE `userdb`.`improvs` (
    `id` INT NOT NULL AUTO_INCREMENT,
     `name` VARCHAR(500),
     `XML` MEDIUMTEXT NULL,
      PRIMARY KEY (`id`));'''

    cursor = mydb.cursor()
    cursor.execute(query_create_improvs_table)
    mydb.commit()

    query_create_xml_table = '''CREATE TABLE `userdb`.`XMLTable` (
    `id` INT NOT NULL AUTO_INCREMENT,
     `name` VARCHAR(500),
     `XML` MEDIUMTEXT NULL,
      PRIMARY KEY (`id`));'''

    cursor.execute(query_create_xml_table)
    mydb.commit()

    path_of_the_directory = 'charlie_parker'  # full directory path of musicXML files
    items_in_folder = os.listdir(path_of_the_directory)
    # print(items_in_folder)
    for filename in items_in_folder:
        f = os.path.join(path_of_the_directory, filename)
        if os.path.isfile(f):
            if f.endswith('.xml'):
                with open(f, 'r') as f:
                    xmlData = f.read()

                insert_query = f"INSERT INTO xmlTable (XML, name) VALUES (%s, %s)"
                values = (xmlData, filename)
                cursor.execute(insert_query, values)

                mydb.commit()


if __name__ == 'main':
    # run from here
    createDB()
    createTables()
