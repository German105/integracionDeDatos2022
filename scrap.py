import requests
import csv
from bs4 import BeautifulSoup

baseUrl= 'https://www.gub.uy/'

def getArticle(link):
    dir = baseUrl + link
    r = requests.get(dir)
    content = BeautifulSoup(r.content, "html.parser")

    title = content.find('h2', attrs={'class':'Page-Title'})
    title = title.text.strip()
    date = content.find('div', attrs={'class':'Page-date'})
    date = date.text.strip()

    pd = content.find('div', attrs={'class':'Page-document page-news'})
    ps = pd.find_all('p')
    body = ''
    for i in ps:
        body = body + i.text.strip() + '\n'

    article = (dir, title, date, body)
    return article

def getLinks(link):
    r = requests.get(link)
    content = BeautifulSoup(r.content, "html.parser")

    boxes = content.find_all('h3', attrs={'class':'Box-title'})
    result = []
    for i in boxes:
        result.append(i.find('a')['href'])
    return result


def main():
    url = 'https://www.gub.uy/presidencia/comunicacion/noticias'
    page = 'https://www.gub.uy/presidencia/comunicacion/noticias?page='

    articlesLinks = []
    target = range(100)
    for i in target:
        articlesLinks = articlesLinks + getLinks(page + str(i))
    print('Links done')

    corpus = []
    for i in articlesLinks:
        corpus.append(getArticle(i))
    print('Articles done')

    f = open('articulos.csv', 'w')
    writer = csv.writer(f, delimiter='	')
    for r in corpus:
        writer.writerow(list(r))
    f.close()
    print('Done')
main()
