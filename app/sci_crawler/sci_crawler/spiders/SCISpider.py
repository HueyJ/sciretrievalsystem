import scrapy
import json
import string
from urllib.parse import quote_plus, unquote_plus
from sci_crawler.items import SciCrawlerItem

class SCISpider(scrapy.Spider):
    name = "SCI"


    def __init__(self, query=""):
        if query is None:
            self.query = ""
        else:
            self.query = quote_plus(query)
            self.filename = query


    def start_requests(self):
        urls = [
            "https://api.elsevier.com/content/search/sciencedirect" +
            "?" + "query=" +
            # "https://api.elsevier.com/content/article/pii/" +
            self.query
            # + "?httpAccept=application/json"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response_dict = json.loads(response.body)
        if response_dict.get("search-results"):
            results = response_dict["search-results"]
            documents = results["entry"]
            for document in documents:
                article_url = document["prism:url"]
                if article_url is not None:
                    article_url = response.urljoin(article_url) + \
                                    "?httpAccept=application/json"
                yield scrapy.Request(url=article_url, callback=self.parse)

            # links = results["link"]
            # if links[-2]["@ref"] == "next":
            #     next_page = links[-2]["@href"]
            # else:
            #     for link in links:
            #         if link["@ref"] == "next":
            #             next_page = link["@href"]
            # if next_page is not None:
            #     next_page = response.urljoin(next_page)
            #     yield scrapy.Request(next_page, callback=self.parse)


        # if the content crawled is article, parse it
        if response_dict.get("full-text-retrieval-response"):
            document = response_dict["full-text-retrieval-response"]["coredata"]
            item = SciCrawlerItem()
            punc_tab = str.maketrans("", "", string.punctuation)
            item["id"] = document["pii"].translate(punc_tab)
            yield self.__process(item, document)




    def __process(self, item, document):
        # fields that should be specifically processed
        document_fields = \
            ("link", "dcterms:subject", "dc:description", "dc:creator") + \
            ("openaccess", "dc:title", "pii", "eid", "prism:publicationName",
            "prism:volume", "prism:startingPage", "prism:endingPage",
            "prism:coverDate", "prism:doi", "prism:aggregationType",
            "prism:issn", "prism:pageRange")
        for key, value in document.items():
            if key is None or key not in document_fields or value is None:
                continue
            if key == "link":
                key = "href"
                value = self.__process_link(value)
            if key == "dcterms:subject":
                value = self.__process_subject(value)
            if key == "dc:description":
                key = "abstract"
                value = self.__process_description(value)
            if key == "dc:creator":
                key = "author"
                value = self.__process_creator(value)
            key = key.split(":")[-1].replace("-", "_")
            item[key] = value
        return item

    def __process_link(self, links):
        for link in links:
            if link["@rel"] == "scidir":
                return link["@href"]

    def __process_subject(self, subjects):
        return self.__extract(subjects)

    def __process_description(self, description):
        description = description.replace("\n", "").replace("  ", "").strip()
        if description.startswith("Abstract"):
            description = description[len("Abstract"):].strip()
        return description

    def __process_creator(self, authors):
        return self.__extract(authors, if_switch=True)

    def __extract(self, items, if_switch=False):
        result = ""
        if isinstance(items, dict):
            if if_switch:
                switch = items["$"].split(", ")
                items["$"] = switch[-1] + " " + switch[0]
            result += items["$"] + ", "
        else:
            for item in items:
                if if_switch:
                    switch = item["$"].split(", ")
                    item["$"] = switch[-1] + " " + switch[0]
                result += item["$"] + ", "
        return result.rstrip()[:-1] + ";"
