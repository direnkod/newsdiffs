from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

import datetime

class ZamanParser(BaseParser):
    SUFFIX = ''
    domains = ['www.zaman.com.tr']

    end_date = datetime.date.today().isoformat()
    start_date = (datetime.date.today()-datetime.timedelta(days=1)).isoformat()

    feeder_pat   = '^http://www.zaman.com.tr/.*\.html$'
    feeder_pages = ['http://www.zaman.com.tr/menuDetail.action?archiveDate=%s&sectionId=3052' % start_date]

    # print feeder_pages

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        print 'at the beginning'
        self.meta = soup.findAll('meta')
        elt = soup.find("h1", attrs={"itemprop": "name"})
        if elt is None:
            self.real_article = False
            return
        print 'after title'
        self.title = elt.getText()
        print self.title
        self.byline = ''
        self.date = soup.find('div', attrs={'class': 'detayTarih'}).getText()

        yazar = soup.find('div', attrs={'class': 'yazarWrap'})

        if yazar is None:
            div = soup.find('div', attrs={'class': 'detayText'})
        else:
            div = soup.find('div', attrs={'class': 'tab-content yazarContent'})
        if div is None:
            # Hack for video articles
            div = soup.find('div', 'emp-decription')
        if div is None:
            self.real_article = False
            return
        if yazar is None:
            tmp = div.find('span', attrs={'class': 'detayMuhabir'})
            if tmp is not None:
                self.body = 'Muhabir: ' + tmp.getText()
            else:
                self.body = 'Muhabir: ' + 'YOK'
        else:
            self.body = 'Yazar: ' + yazar.find('h5', attrs={'itemprop': 'name'}).getText()
        #self.body = self.body + '\n'+'\n\n'.join([x.getText() for x in div.childGenerator()
        #                              if isinstance(x, Tag) and x.name == 'p'])
        self.body = self.body + '\n'+'\n\n'.join([x.getText() for x in div.findAll('p')])
