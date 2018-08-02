'''
@author: th0rben
'''
import sqlite3
import smtplib
import datetime
import sys
from html_downloader import create_article_dictionary, find_all_articles
from database_maintainer import add_article, initilize_database
from login_data import sender, recipient, password
from login_data import subject, server, port



# send text as email
def sendmail(text):
    smtp_server = smtplib.SMTP_SSL(server, port)
    smtp_server.login(sender, password)
    message = "Subject: {}\n\n{}".format(subject, text)
    smtp_server.sendmail(sender, recipient, message)
    smtp_server.close()

# saves all articles which mentioned
# as url in root_url
# return text including all saved 
# articles and all potential errors
def save_articles_sqllite(root_url):
    initilize_database()
    articles_urls = find_all_articles(root_url)
    connection = sqlite3.connect("articles.db")
    articles_quantity = len(articles_urls)
    now = str(datetime.datetime.now()) + '\n'
    log = '----- \n start downloading at: ' + now
    try:
        for i in range (0,articles_quantity):
            url = articles_urls[i]
            log = log + str(i+1)+'/'+str(articles_quantity)+ ' ' + url + '\n'
            article_array = create_article_dictionary(url)
            connection = add_article(connection, article_array)
        message = now + ' ' + str(articles_quantity) + ' articles successfully downloaded'
    except:
        message = now + 'ERROR: \n'
        e = sys.exc_info()[0]
        message = message + str(e) + ' at ' + url
    logging(log)
    return message

# write log to file
def logging(text):
    file = open('downloads.log','w') 
    file.write(text) 
    file.close()
    
def main():
    root_url = 'https://www.bild.de/'
    text = save_articles_sqllite(root_url)
    sendmail(text)
    #print(text)

main()