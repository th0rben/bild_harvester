'''
@author: th0rben
'''
from bild_harvester.html_downloader import create_article_dictionary, find_all_articles
from bild_harvester.database_maintainer import add_article, initilize_database
import sqlite3
#import schedule
#import time

def main():
    initilize_database()
    articles_urls = find_all_articles('https://www.bild.de/')
    connection = sqlite3.connect("articles.db")
    articles_quantity = len(articles_urls)
    print('start downloading...')
    for i in range (0,articles_quantity):
        print('downloading: ',str(i+1),'/',str(articles_quantity), end=' ', flush=True)
        article_array = create_article_dictionary(articles_urls[i])
        connection = add_article(connection, article_array)
    print('downloading completed')

main()

#https://stackoverflow.com/a/30393162
#this script executes the harvester every day at 1:00
#schedule.every().day.at("01:00").do(main)
#while True:
#    schedule.run_pending()
#    time.sleep(60) # wait one minute