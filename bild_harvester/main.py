'''
@author: th0rben
'''
from bild_harvester.html_downloader import create_article_dictionary, find_all_articles
from bild_harvester.database_maintainer import add_article, initilize_database
import sqlite3
import smtplib

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
    smtp_server = smtplib.SMTP_SSL(server, port)
    smtp_server.login(sender, password)
    message = "Subject: {}\n\n{}".format(subject, text)
    smtp_server.sendmail(sender, recipient, message)
    smtp_server.close()

main()