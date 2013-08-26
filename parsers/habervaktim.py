from baseparser import BaseParser
from BeautifulSoup import BeautifulSoup, Tag

class HaberVaktimParser(BaseParser):
    domains = ['www.habervaktim.com']

    feeder_pat   = '^http://www.habervaktim.com/(haber|yazar)/\d+'
    feeder_pages = ['http://www.habervaktim.com']

    def _parse(self, html):
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES,
                             fromEncoding='utf-8')

        self.body = ""
        self.byline = ""

        news_content_css_id = "news_content"
        body = soup.find('div', attrs={'id': 'base_middle'})
        author = body.find('div', attrs={'class': 'middle_page_title'})
        if author:
            # Author article
            self.byline = author.find("h1").getText()
            news_content_css_id = "author_article_content"

        content = body.find('div', attrs={'class' : 'middle_content'})
        short_content = content.find('div', attrs={'class' : 'short_content'})
        if short_content:
            self.body = short_content.getText() + "\n"
        self.title = content.find('div', attrs={'class' : 'title'}).getText()
        self.date = content.find('div', attrs={'class' : 'date'}).getText()

        news_content = content.find('div', attrs={'id' : news_content_css_id}).findAll("p")
        tags = [("b", None), ("strong", None), ("em", None), ("br", "\n"), ("a", None)]
        for p in news_content:
            for tag, subs in tags:
                for match in p.findAll(tag):
                    if subs:
                        match.replaceWith(subs)
                    else:
                        match.replaceWithChildren()
            self.body += "\n" + p.getText() + "\n"
