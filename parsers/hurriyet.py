from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

import datetime

class HurriyetParser(BaseParser):
    domains = ['www.hurriyet.com.tr']

    feeder_pat   = '^http://www.hurriyet.com.tr/(.*)/[0-9]*\.asp'
    feeder_pages = ['http://www.hurriyet.com.tr']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        self.body = ""

        # Fetch date
        self.date = soup.find("div", {"class": "HaberDetayDate txtLeft"}).getText()

        # Fetch title
        self.title = soup.find("div", {"class": "HaberDetayTitleHold Title"}).getText()

        # Summary
        summary = soup.find("div", {"class": "HaberDetaySpotText"})
        if summary:
            self.body = summary.getText() + "\n\n"

        # Get reporter (muhabir)
        info = soup.find("div", {"class": "HaberDetayInfo txtLeft"})
        if info:
            self.byline = info.getText()

        for pgraph in soup.find("div", {"id": "DivAdnetHaberDetay"}).find("div",
                {"class": "txt"}).findAll("p", recursive=False):
            for elem in pgraph:
                try:
                    if elem.name == "br":
                        self.body += "\n"
                    elif elem.name == "strong":
                        # There are sometimes links to other news, drop them
                        if elem.find("a"):
                            elem.find("a").extract()
                        self.body += "\n" + elem.getText() + "\n"
                    else:
                        self.body += elem.getText()
                except AttributeError, e:
                    self.body += unicode(elem)
            self.body += "\n"
