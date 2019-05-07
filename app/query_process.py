from flask import current_app
import os

class QueryProcessor:

    def process(self, search_terms, start=1):
        return self.__query(search_terms, start)["hits"]["hits"]

    def __query(self, search_terms, start=1):
        if not current_app.es:
            return []
        query_expression = ""
        # for stem in stems:
        #     query_expression += stem + " "
        print(search_terms)
        size = 100
        query = {
            "from": (start - 1) * size, "size": size,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match_phrase": {
                                "eid": {"query": search_terms, "boost": 1000}
                            }
                        },
                        {
                            "match_phrase": {
                                "doi": {"query": search_terms, "boost": 1000}
                            }
                        },
                        {
                            "match_phrase": {
                                "pii": {"query": search_terms, "boost": 1000}
                            }
                        },
                        {
                            "match_phrase": {
                                "id": {"query": search_terms, "boost": 1000}
                            }
                        },
                        {
                            "match_phrase": {
                                "author": {"query": search_terms, "boost": 1000}
                            }
                        }
                    ],
                    "must": [
                        {
                            "multi_match": {
                                "query": search_terms,
                                "fields": [
                                    "title",
                                    "abstract",
                                    "subject"
                                ],
                                "fuzziness": 1
                            }
                        }
                    ]
                }
            }
        }
        return current_app.es.search(query)
