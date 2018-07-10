'''
@author: th0rben
'''
from bild_harvester.html_downloader import download, find_all_articles
from bild_harvester.database_maintainer import add_article, get_all_articles, get_all_tables, initilize_database
import sqlite3

def main():
    initilize_database()
    articles_urls = find_all_articles('https://www.bild.de/news/startseite')
    connection = sqlite3.connect("articles.db")
    for url in articles_urls:
        article_array = download(url)
        connection = add_article(connection, article_array)
    get_all_articles(connection)


    
main()