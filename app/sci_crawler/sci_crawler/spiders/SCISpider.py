import scrapy
import json
from urllib.parse import quote_plus
from sci_crawler.items import SciCrawlerItem

class SCISpider(scrapy.Spider):
    name = "SCI"
    document_fields = ("load-date","prism:url", "openaccess", "dc:title", "pii",
        "prism:publicationName", "prism:volume", "prism:startingPage", "link",
        "prism:endingPage", "prism:coverDate", "dc:creator", "prism:doi",
        "authors")

    def __init__(self, query=""):
        if query is None:
            self.query = ""
        else:
            self.query = quote_plus(query)
            self.filename = query


    def start_requests(self):
        urls = [
            "https://api.elsevier.com/content/search/sciencedirect" + "?"
            "query=" + self.query
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open("test2.json", "wb") as f:
            f.write(response.body)
        results = json.loads(response.body)["search-results"]
        documents = results["entry"]
        for document in documents:
            item = SciCrawlerItem()
            yield self.__process_item(item, document)

        links = results["link"]
        if links[-2]["@ref"] == "next":
            next_page = links[-2]["@href"]
        else:
            for link in links:
                if link["@ref"] == "next":
                    next_page = link["@href"]
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def __process_item(self, item, document):
        for key, value in document.items():
            if key is None or key not in self.document_fields\
                or value is None:
                continue
            if key == "link":
                value = value[1]["@href"].split("?")[0]
            if key == "authors":
                authors = ""
                for key, author_names in value.items():
                    if not isinstance(author_names, str):
                        for author_name in author_names:
                            authors += author_name["$"] + ", "
                    else:
                        authors = author_names + ", "
                authors = authors.rstrip()
                authors = authors[:-1] + "."
                value = authors
                value = value.rstrip()[:-1]
            key = key.split(":")[-1].replace("-", "_")
            item[key] = value
        return item
