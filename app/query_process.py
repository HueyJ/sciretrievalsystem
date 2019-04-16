from redis import Redis, ConnectionPool
from redis.exceptions import ConnectionError
from porter_stemmer import PorterStemmer
from flask import current_app
import os

class QueryProcessor:

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    REDIS_DECODE_RES = os.environ.get('REDIS_DECODE_RES')

    redis_operator = None
    stemmer = None

    def __init__(self):
        if not self.redis_operator:
            self.redis_operator = RedisOperator(self.REDIS_HOST, self.REDIS_PORT,
                                    self.REDIS_DECODE_RES).get_instance()

        if not self.stemmer:
            self.stemmer = Stemmer()

    def process(self, search_terms):
        results = []
        stems = self.__stem(self.__tokenize(search_terms))
        for stem in stems:
            try:
                if self.redis_operator.check(stem):
                    self.redis_operator.add(stem)
                    # TODO print(self.es.)
                else:
                    self.redis_operator.add(stem)
                    print("send search request to scrapy first, and then get the results from backend")
            except (ConnectionError, ConnectionRefusedError):
                    print("Connect to Redis failed.")
        return results

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
        stems = []
        for token in tokens:
            stem = self.stemmer.stem(token)
            stems.append(stem)
        return stems

class RedisOperator:
    instance = None

    def __init__(self, redis_host='localhost', redis_port=6379,
                 redis_decode_res=True):
        if not self.instance:
            RedisOperator.instance = RedisOperator.__RedisOperator(redis_host,
                                                     redis_port,
                                                     redis_decode_res)
    def get_instance(self):
        return self.instance

    class __RedisOperator:
        pool = None

        def __init__(self, redis_host, redis_port, redis_decode_res):
            if not self.pool:
                self.pool = ConnectionPool(host=redis_host, port=redis_port,
                                decode_responses=redis_decode_res)

        def add(self, query):
            return Redis(connection_pool=self.pool).incr(query, amount=1)

        def check(self, query):
            return Redis(connection_pool=self.pool).get(query)


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
