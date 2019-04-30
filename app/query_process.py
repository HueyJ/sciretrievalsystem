from porter_stemmer import PorterStemmer
from flask import current_app
from es_processor import ESProcessor
import os

class QueryProcessor:

    stemmer = None

    def __init__(self):
        if not self.stemmer:
            self.stemmer = Stemmer()

    def process(self, search_terms):
        # stems = self.__stem(self.__tokenize(search_terms))
        # print(stems)
        # for stem in stems:
        #     try:
        #         if current_app.redis.check(stem):
        #             self.redis_operator.add(stem)
        #         else:
        #             self.redis_operator.add(stem)
        #             print("send search request to scrapy first, and then get the results from backend")
        #     except (ConnectionError, ConnectionRefusedError):
        #             print("Connect to Redis failed.")
        return self.__query(search_terms)["hits"]["hits"]

    def __tokenize(self, raw_text):
        # split words into words use punctuation
        import re
        tokens = re.split(r"\W+", raw_text)
        # convert words to lower case
        tokens = [w.lower() for w in tokens]
        # remove punctuation
        import string
        punc_tab = str.maketrans("", "", string.punctuation)
        tokens = [w.translate(punc_tab) for w in tokens]
        # remove remaining tokens that are not alphabetic or number
        tokens = [w for w in tokens if w.isalnum()]
        # filter out stop words
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words("english"))
        tokens = [w for w in tokens if not w in stop_words]
        return tokens

    def __stem(self, tokens):
        print(tokens)
        stems = []
        for token in tokens:
            stem = self.stemmer.stem(token)
            stems.append(stem)
        return stems

    def __query(self, search_terms):
        if not current_app.es:
            return []
        query_expression = ""
        # for stem in stems:
        #     query_expression += stem + " "
        print(search_terms)
        query = {
            'query': {
                'multi_match': {
                    'query': search_terms,
                    'fields': [
                        'title^10', 'abstract', 'subject^5'
                    ],
                    "fuzziness": "3"
                }
            }
        }
        return current_app.es.search(query)

class Stemmer:

    suffiexes_striper = None

    def __init__(self):
        self.suffiexes_striper = PorterStemmer()

    def stem(self, word):
        word = word.strip()
        if word is not "" and len(word) > 2:
            word = self.__strip_prefixes(word)
            if word is not "":
                word = self.__strip_suffiexes(word)
        return word

    def __strip_prefixes(self, word):
        prefixes = {"kilo", "micro", "milli", "intra", \
                    "ultra", "mega", "nano", "pico", "pseudo"}

        for prefix in prefixes:
            if word.startswith(prefix):
                word = word[len(prefix):]

        return word

    def __strip_suffiexes(self, word):
        word = self.suffiexes_striper.stem(word, 0, len(word)-1)
        return word
