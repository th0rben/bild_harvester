'''
@author: th0rben
'''
import sqlite3

#sets up an SQLLite Database 'articles'
#creates table: 'articles' in the database
def initilize_database():
    connection = sqlite3.connect("articles.db")

    cursor = connection.cursor()
    sql_command = """
    CREATE TABLE IF NOT EXISTS articles ( 
    url VARCHAR(250),
    article_id INTEGER NOT NULL,
    category VARCHAR(50),
    sub_category VARCHAR(50),
    author VARCHAR(100),
    datePublished TIME,
    dateModified TIME,
    keywords VARCHAR(200),
    isFamilyFriendly VARCHAR(5),
    headline VARCHAR(100),
    description VARCHAR(100), 
    text VARCHAR(2000),
    PRIMARY KEY (article_id));"""

    cursor.execute(sql_command)
    connection.commit()
    return connection

#adds an article in to the database
#the article data is in article_dictionary
#article_dictionary needs to be well formed
def add_article(connection, article_dictionary):
    cursor = connection.cursor()
    
    format_str = """INSERT OR IGNORE INTO articles (url, article_id, category, sub_category, author,
    datePublished, dateModified, keywords, isFamilyFriendly, headline, description, text)
    VALUES ("{url}", "{article_id}", "{category}", "{sub_category}", "{author}", "{datePublished}", "{dateModified}",
    "{keywords}", "{isFamilyFriendly}", "{headline}", "{description}", "{text}");"""
    sql_command = format_str.format(
        url=article_dictionary['url'], article_id=int(article_dictionary['article_id']), 
        category=article_dictionary['category'], sub_category=article_dictionary['sub_category'], 
        author=article_dictionary['author']['name'], datePublished=article_dictionary['datePublished'], 
        dateModified=article_dictionary['dateModified'], keywords=article_dictionary['keywords'], 
        isFamilyFriendly=article_dictionary['isFamilyFriendly'], headline=article_dictionary['headline'], 
        description=article_dictionary['description'], text=article_dictionary['text'])
    
    cursor.execute(sql_command)
    connection.commit()
    return connection

#print every row in the tables: 'articles'
def print_all_articles(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM articles") 
    print("fetchall:")
    result = cursor.fetchall() 
    for r in result:
        print(r)
