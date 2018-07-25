'''
@author: th0rben
'''
from bild_harvester.html_downloader import create_article_dictionary, find_all_articles
from bild_harvester.database_maintainer import add_article, initilize_database
import sqlite3
import smtplib
import datetime
from login_data import sender, recipient, password
from login_data import subject, server, port

def main():
    root_url = 'https://www.bild.de/'
    text = save_articles_sqllite(root_url)
    sendmail(text)

def sendmail(text):
    smtp_server = smtplib.SMTP_SSL(server, port)
    smtp_server.login(sender, password)
    message = "Subject: {}\n\n{}".format(subject, text)
    smtp_server.sendmail(sender, recipient, message)
    smtp_server.close()
    
def save_articles_sqllite(root_url):
    initilize_database()
    articles_urls = find_all_articles(root_url)
    connection = sqlite3.connect("articles.db")
    articles_quantity = len(articles_urls)
    text = 'start downloading at: ' 
    text = text + str(datetime.datetime.now()) + '...\n'
    for i in range (0,articles_quantity):
        url = articles_urls[i]
        text = text + str(i+1)+'/'+str(articles_quantity)+ ' ' + url + '\n'
        article_array = create_article_dictionary(url)
        connection = add_article(connection, article_array)
    now = str(datetime.datetime.now())
    text = text + 'downloading successfully finished at ' + now
    return text

main()