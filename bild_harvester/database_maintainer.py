'''
@author: th0rben
'''
import sqlite3

def initilize_database():
    connection = sqlite3.connect("articles.db")

    cursor = connection.cursor()
    # delete 
    #cursor.execute("""DROP TABLE employee;""")

    sql_command = """
    CREATE TABLE articles ( 
    article_id INTEGER NOT NULL,
    title VARCHAR(100), 
    author VARCHAR(100),
    place VARCHAR(50),
    publication_time TIME,
    text VARCHAR(2000),
    PRIMARY KEY (article_id));"""

    cursor.execute(sql_command)

    # never forget this, if you want the changes to be saved:
    connection.commit()
    return connection

def add_article(connection, article_array):
    cursor = connection.cursor()
    #sql_command = """INSERT INTO articles (article_id, title, author, place, publication_time, text)
    #VALUES (123, "Titel", "Autor", "hier", "2018-07-05T21:56:34+02:00","Text");"""
    
    format_str = """INSERT INTO articles (article_id, title, author, place, publication_time, text)
    VALUES ("{article_id}", "{title}", "{author}", "{place}", "{publication_time}", "{text}");"""
    sql_command = format_str.format(article_id=int(article_array[0]), title=article_array[1], author=article_array[2], place = article_array[3], publication_time = article_array[4], text = article_array[5])
    cursor.execute(sql_command)
    connection.commit()
    return connection

def get_all_articles(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM articles") 
    print("fetchall:")
    result = cursor.fetchall() 
    for r in result:
        print(r)
        
def get_all_tables(connection):
    cursor = connection.cursor()
    sql_command = """SELECT name FROM sqlite_master
    WHERE type='table';"""
    cursor.execute(sql_command)
    connection.commit()

    connection.close()
    return connection