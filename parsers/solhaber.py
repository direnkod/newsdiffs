from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

import datetime

class SolHaberParser(BaseParser):
    SUFFIX = ''
    domains = ['haber.sol.org.tr']

    end_date = datetime.date.today().isoformat()
    start_date = (datetime.date.today()-datetime.timedelta(days=1)).isoformat()

    feeder_pat   = '^http://haber.sol.org.tr/'
    feeder_pages = ['http://haber.sol.org.tr/arsiv?icerik=All&tarih%%5Bmin%%5D%%5Bdate%%5D=%s&tarih%%5Bmax%%5D%%5Bdate%%5D=%s' % (start_date, end_date)]

    # print feeder_pages

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        print 'at the beginning'
        self.meta = soup.findAll('meta')
        elt = soup.find("h2", attrs={"class": "title node-title"})
        if elt is None:
            self.real_article = False
            return
        print 'after title'
        self.title = elt.getText()
        print self.title
        self.byline = ''
        self.date = soup.find('div', attrs={'class': 'node-date'}).getText()

        div = soup.find('div', attrs={'class': 'makale-govde'})
        print div
        if div is None:
            # Hack for video articles
            div = soup.find('div', 'emp-decription')
        if div is None:
            self.real_article = False
            return
        self.body = '\n'+'\n\n'.join([x.getText() for x in div.childGenerator()
                                      if isinstance(x, Tag) and x.name == 'p'])
