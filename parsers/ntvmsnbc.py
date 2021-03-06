from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

import datetime

class NTVMSNBCParser(BaseParser):
    domains = ['www.ntvmsnbc.com']

    feeder_pat   = '^http://www.ntvmsnbc.com/id/\d+/'
    feeder_pages = ['http://www.ntvmsnbc.com']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        div_content = soup.find("div", {"id" : "content"})

        try:
            self.title = div_content.find("h1").getText()
        except AttributeError, ae:
            # We're in top-story pages, skip
            self.real_article = False
            return

        self.byline = ""
        self.date = div_content.find("span", {"class" : "date"}).getText().replace(".", "")
        self.date += " " + div_content.find("span", {"class" : "time"}).getText()

        byline = div_content.find("div", {"class" : ["textMedBlack", "textMedBlackBold"]})
        if byline:
            strongs = byline.findAll("strong")
            # Fix for stupid ntvmsnbc
            if strongs:
                self.byline = strongs[-1].getText()
            else:
                self.byline = byline.getText()

        # Summary
        self.body = div_content.find("h2").getText() + "\n"

        tags = [("b", None), ("strong", None), ("br", "\n\n")]
        for p in div_content.findAll("p", {"class" : "textBodyBlack"}):
            for tag, subs in tags:
                for match in p.findAll(tag):
                    if subs:
                        match.replaceWith(subs)
                    else:
                        match.replaceWithChildren()
            self.body += "\n" + p.getText() + "\n"
