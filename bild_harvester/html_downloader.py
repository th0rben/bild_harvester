'''
@author: th0rben
'''
import urllib.request
import re
from bs4 import BeautifulSoup

def find_all_articles(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary)
    soup = BeautifulSoup(text, 'html.parser')
    articles_urls = []
    for a in soup.find_all('a', href=True, rel='bookmark'):
        href = a['href']
        if not (href.startswith("/video") or href.startswith("/bild-plus") or ("/startseite/" in href)):
            articles_urls.append('https://www.bild.de'+href)
        
    return articles_urls

def download(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary)
    soup = BeautifulSoup(text, 'html.parser')
    title_place = soup_to_title_place(soup)
    article_id = url[::-1].split('.')[2].split('-')[0][::-1]
    title = title_place[1]
    author = get_author(soup)
    datetime = get_datetime(soup)
    place = title_place[0].split(':')[0]
    text = soup_to_clean_text(soup)
    article_array = []
    article_array.append(article_id)
    article_array.append(title)
    article_array.append(author)
    article_array.append(datetime)
    article_array.append(place)
    article_array.append(text)
    return article_array
        

def soup_to_clean_text(soup):
    text = str(soup.find_all("div", class_="txt")[0].find_all('p'))
    advertisements = soup.find_all("p", class_="entry-content")
    links = soup.find_all('a')
    
    #removes the advertisement between the text
    for i in range (0,len(advertisements)):
        text = text.replace(str(advertisements[i]), '')
    
    #removes the links at the end of the text
    for i in range (0,len(links)):
        text = text.replace(str(links[i]), '')
        
    #removes sentences at the end of the text
    text = text.replace('<p><strong><em>Hier geht es zurück zu </em></strong></p>', '')

    text = cleanhtml(text)
    
    #removes spare commas which are produced by previous steps
    text = text.replace(" , , ", '')
    text = text.replace(".,", '.')
    
    # removes place at the beginning of the text
    text_split = text.split(' – ')
    if len(text_split) > 1:
        text = text_split[1]
    
    # removes space brackets at the end of the text
    text = text.replace(']','')
    text = text.replace('"',"'")
    return text

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

def get_author(soup):
    author = soup.find_all("span", class_="authors__name")
    if (author == []):
        print("no author")
        return ""
    else:
        return cleanhtml(str(soup.find_all("span", class_="authors__name")[0]))

def get_datetime(soup):
    datetime = str(soup.find_all("time", class_="authors__pubdate")[0])
    datetime = datetime.replace('<time class="authors__pubdate" datetime="','').split('">')[0]
    return datetime


