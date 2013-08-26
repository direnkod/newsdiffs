from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag, NavigableString

import datetime

class AAParser(BaseParser):
    domains = ['www.aa.com.tr']

    feeder_pat   = '^http://www.aa.com.tr/tr/(.*)/[0-9]*--.*$'
    feeder_pages = ['http://www.aa.com.tr']

    exclude_pattern = ["kurumsal.*/", "mod/", "aa-hizmetler/"]
    basename_filter = True

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        body = soup.find("div", {"id" : "printBody"})
        header = body.find("div", {"class" : "news-kunye"})

        if not header:
            self.real_article = False
            return

        # byline parsing is problematic, skip.
        self.byline = ""

        self.title = header.find("h3").getText()
        self.date = header.find("div", {"class" : "kunye"}).find("span").getText()

        news_content = body.find("div", {"id" : "news-maincontent"}).findAll("p")

        # Prepend summary
        self.body = body.find("div", {"class" : "news-spot"}).getText() + "\n\n"

        tags = [("b", None), ("strong", None), ("em", None), ("br", "\n\n"), ("a", None)]
        for p in news_content:
            for tag, subs in tags:
                for match in p.findAll(tag):
                    if subs:
                        match.replaceWith(subs)
                    else:
                        match.replaceWithChildren()
            self.body += "\n" + p.getText() + "\n"
