import urllib.request
import re
from bs4 import BeautifulSoup

url = 'https://www.bild.de/regional/chemnitz/isis-terroristen/der-islamist-der-sieben-mal-im-jahr-geburstag-hat-56228350.bild.html'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary)
soup = BeautifulSoup(text, 'html.parser')

def soup_to_clean_text(soup):
    text = str(soup.find_all("div", class_="txt")[0].find_all('p'))
    advertisements = soup.find_all("p", class_="entry-content")
    links = soup.find_all('a')
    
    #removes the advertisement between the text
    i = 0
    while i < len(advertisements):
        text = text.replace(str(advertisements[i]), '')
        i = i+1
    
    #removes the links at the end of the text
    j = 0
    while j < len(links):
        text = text.replace(str(links[j]), '')
        j = j+1
        
    #removes sentences at the end of the text
    text = text.replace('<p><strong><em>Hier geht es zurück zu </em></strong></p>', '')
    cleantext = cleanhtml(text)
    return cleantext

# removes any tags in delimiters
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('\r', '').replace('\n', '')
    return cleantext

# generates array containing title and place of the article from soup
def soup_to_title_place(soup):
    title = str(soup.title)
    clean_title = cleanhtml(title).replace('\t', '')
    return clean_title.split('-')


title_place = soup_to_title_place(soup)
title = title_place[1]
place = title_place[0].split(':')[0]
text = soup_to_clean_text(soup)


file = open("testfile.html","w")  
file.write(text)
file.close() 