'''
@author: th0rben
'''
import urllib.request
import json
import re
from bs4 import BeautifulSoup

#finds all articles in an url
# e. g. 'https://www.bild.de/'
#ignores pages of categories and advertisement
def find_all_articles(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary)
    soup = BeautifulSoup(text, 'html.parser')
    articles_urls = []
    for a in soup.find_all('a', href=True, rel='bookmark'):
        href = a['href']
        if  not (href.startswith("/video") 
                 or href.startswith("/bild-plus") 
                 or ("/startseite/" in href) 
                 or ("/ombudsmann/" in href) 
                 or ("dealsblock" in href) 
                 or ("geld/mein-geld/mein-geld/" in href) 
                 or ("ateaserseite" in href)
                 or ("bildconnect" in href) 
                 or ("corporate-site" in href) 
                 or ("epaper" in href)
                 or ("shop.bild.de" in href)
                 or ("shop.bildplus.de" in href)
                 or ("video-serie" in href) 
                 or ("sport.bild.de" in href) 
                 or ("/home-" in href) 
                 or ("https://www." in href)):
            articles_urls.append('https://www.bild.de'+href)
        
    return articles_urls

#creates article dictionary from url
#url must contains an article which
#has an application/ld+json script
def create_article_dictionary(url):
    response = urllib.request.urlopen(url)
    data = response.read()      # a `bytes` object
    text = data.decode('utf-8') # a `str`; this step can't be used if data is binary)
    soup = BeautifulSoup(text, 'html.parser')
    article_json = soup.find('script', {'type':'application/ld+json'})
    article_dictionary = json.loads(str(article_json).replace('<script type="application/ld+json">', '').replace('</script>', ''), strict=False)
    #excludes overviews over articles
    if (article_dictionary['@type']==('Organization')):
        article_dictionary = "no_article"
    else:
        article_dictionary['article_id'] = url[::-1].split('.')[2].split('-')[0][::-1]
        article_dictionary.update(get_category_subcategory(url))
        article_dictionary['text'] = soup_to_clean_text(soup)
    
    return article_dictionary

#cuts out category and subcategory from url
def get_category_subcategory(url):
    category_subcategory = url.replace('https://www.bild.de','').replace('/news','').split('/')
    return {"category":category_subcategory[1],"sub_category":category_subcategory[2]}

#extracts article text from soup
#removes any kind of noise:
#advertisement and tags
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
    
    text = remove_tags(text)
    
    #removes spare commas which are produced by previous steps
    text = text.replace(" , , ", '').replace(".,", '.').replace('PS: Sind Sie bei Facebook? !', '')
    
    # removes space brackets at the end of the text
    text = text.replace(']','').replace('[','').replace('"',"'")
    return text

#remove everything in delimiters and delimiters
def remove_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('\r', '').replace('\n', '')
    return cleantext