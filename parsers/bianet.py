from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

import datetime

class BIANETParser(BaseParser):
    domains = ['www.bianet.org']

    feeder_pat   = 'bianet.org/bianet/(.*)/[0-9]*-.*'
    feeder_pages = ['http://www.bianet.org']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        headline = soup.find("div", {"class" : "manset"})
        self.title = headline.find("h2").getText()
        self.date = headline.find("div", {"class" : "yer"}).getText()

        author = headline.find("div", {"class" : "isim"})
        if author:
            # Written by specific author
            self.byline = author.getText()
        else:
            # Written by BIANET agency
            self.byline = headline.find("div", {"class" : "from"}).getText()

        # Prepend summary
        self.body = "\n" + headline.find("p").getText() + "\n"

        tags = [("b", None), ("strong", None), ("em", None), ("br", "\n\n"), ("a", None)]

        for p in soup.find("div", {"class" : "item"}).findAll("p"):
            for tag, subs in tags:
                for match in p.findAll(tag):
                    if subs:
                        match.replaceWith(subs)
                    else:
                        match.replaceWithChildren()
            self.body += "\n" + p.getText() + "\n"
