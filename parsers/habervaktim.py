from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

import datetime

class HaberVaktimParser(BaseParser):
    SUFFIX = ''
    domains = ['www.habervaktim.com']

    end_date = datetime.date.today().isoformat()
    start_date = (datetime.date.today()-datetime.timedelta(days=1)).isoformat()

    feeder_pat   = '^http://www.habervaktim.com/haber/\d+'
    feeder_pages = ['http://www.habervaktim.com']

    # print feeder_pages

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        kose_yazisi = soup.find('div', attrs={'class': 'author_article'})

        if kose_yazisi is not None:
            yazar = soup.find('div', attrs={'class': 'middle_page_title'}).find('h1').getText()

        print 'at the beginning'
        self.meta = soup.findAll('meta')
        if kose_yazisi is not None:
            elt = soup.find("div", attrs={"class": "author_article"}).find('div', attrs={"class": "title"})
        else:
            elt = soup.find("div", attrs={"class": "news_detail"}).find('div', attrs={"class": "title"})
        if elt is None:
            self.real_article = False
            return
        print 'after title'
        self.title = elt.getText()
        print self.title
        self.byline = ''
        if kose_yazisi is None:
            self.date = soup.find("div", attrs={"class": "news_detail_content"}).find('div', attrs={"class": "date"}).getText()
        else:
            self.date = soup.find("div", attrs={"class": "author_article"}).find('div', attrs={"class": "date"}).getText()
        if kose_yazisi is not None:
            div = soup.find('div', attrs={'id': 'author_article_content'})
        else:
            div = soup.find('div', attrs={'id': 'news_content'})
        print div
        if div is None:
            # Hack for video articles
            div = soup.find('div', 'emp-decription')
        if div is None:
            self.real_article = False
            return
        self.body = '\n'+'\n\n'.join([x.getText() for x in div.childGenerator()
                                      if isinstance(x, Tag) and x.name == 'p'])
