'''
@author: th0rben
'''
import sqlite3
import smtplib
import datetime
import sys
import os
from html_downloader import create_article_dictionary, find_all_articles
from database_maintainer import add_article, initilize_database, count_table_entries
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
    success_count = 0
    articles_urls = find_all_articles(root_url)
    connection = sqlite3.connect("articles.db")
    articles_quantity = len(articles_urls)
    now = str(datetime.datetime.now()) + '\n'
    log = '----- \n start downloading at: ' + now
    message = now
    for i in range (0,articles_quantity):
        try:
            url = articles_urls[i]
            log = log + str(i+1)+'/'+str(articles_quantity)+ ' ' + url + '\n'
            article_array = create_article_dictionary(url)
            connection = add_article(connection, article_array)
            success_count = success_count + 1
        except:
            e = sys.exc_info()[0]
            message = message + '\n' + str(e) + ' at ' + url + '/n'
    message = message + str(success_count) + ' of '+ str(articles_quantity) + ' detected articles successfully downloaded'

    logging(log)
    return message

# write log to file
def logging(text):
    file = open('downloads.log','w') 
    file.write(text) 
    file.close()

 
def get_file_size(path):
    file_size_bytes = os.path.getsize(path)
    file_size_gigabyte = file_size_bytes / 1000000000
    return "The database is now: " + str(file_size_gigabyte) + "GB large"
    
def main():
    root_url = 'https://www.bild.de/'
    text = save_articles_sqllite(root_url)
    database_size = get_file_size("articles.db")
    connection = sqlite3.connect("articles.db")
    database_entries_quantity = count_table_entries(connection)
    sendmail(text + "\n" + database_size + "\n" + "and contains " + database_entries_quantity + " entries")
    #print(text)

main()