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
    article_id = url[::-1].split('.')[2].split('-')[0][::-1]
    category_subcategory = get_category_subcategory(url)
    category = category_subcategory[0]
    sub_category = category_subcategory[1]
    title = get_title(soup)
    #cleanhtml(str(soup.title)).replace('\t', '').replace('„', "'").replace('“', "'").replace('"', "'").replace('-Bild.de','')
    author = get_author(soup)
    publication_time = get_datetime(soup)
    text = soup_to_clean_text(soup)
    article_array = [article_id, category, sub_category, title, author, publication_time, text]
    return article_array
        
def get_title(soup):
    title_array = cleanhtml(str(soup.title)).replace('\t', '').replace('„', "'").replace('“', "'").replace('"', "'").replace('-Bild.de','').split('-')
    title = str(soup.title).replace(title_array[::-1][0], '').replace('\t', '').replace('Bild.de','').replace('-1414 Leser-Reporter -','')
    title = cleanhtml(title).replace('-1414 Leser','').replace('--','')
    print (title)
    return title

def get_category_subcategory(url):
    category_subcategory = url.replace('https://www.bild.de','').replace('/news','')
    category_subcategory = category_subcategory.split('/')
    category = category_subcategory[1]
    sub_category = category_subcategory[2]
    return [category,sub_category]

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
    text = text.replace('PS: Sind Sie bei Facebook? !', '')
    # removes space brackets at the end of the text
    text = text.replace(']','').replace('[','')
    text = text.replace('"',"'")
    return text

# removes any tags in delimiters
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('\r', '').replace('\n', '')
    return cleantext

def get_author(soup):
    author = soup.find_all("span", class_="authors__name")
    if (author == []):
        return ""
    else:
        return cleanhtml(str(soup.find_all("span", class_="authors__name")[0]))

def get_datetime(soup):
    datetime = str(soup.find_all("time", class_="authors__pubdate")[0])
    datetime = datetime.replace('<time class="authors__pubdate" datetime="','').split('">')[0]
    return datetime


