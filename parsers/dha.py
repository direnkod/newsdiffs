from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

import datetime

class DHAParser(BaseParser):
    domains = ['www.dha.com.tr']

    feeder_pat   = '^http://www.dha.com.tr/.*_[0-9]*\.html'
    feeder_pages = ['http://www.dha.com.tr']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        try:
            self.title  = soup.find("div", {"class": "haberbasligi"}).getText()
        except:
            # This happens on sports news redirecting to sporaktif.dha.com.tr
            self.real_article = False
            return

        self.date   = soup.find("span", {"class": "newsdate"}).getText()
        self.body = ""

        detaytext = soup.find("div", {"id": "detaytext"})
        if detaytext.find("strong"):
            self.byline = detaytext.find("strong").getText()

        in_body = False
        for elem in detaytext:
            if isinstance(elem, NavigableString):
                if in_body:
                    self.body += unicode(elem).strip()
            else:
                # Tag
                if elem.name == "iframe":
                    in_body = True
                elif elem.name == "br" and in_body:
                    self.body += "\n"
                elif elem.name == "b" and in_body:
                    self.body += elem.getText()
                elif elem.name == "div" and in_body:
                    if len(elem.attrs) == 1 and elem.attrs[0][1] == "clear":
                        in_body = False
                        break
