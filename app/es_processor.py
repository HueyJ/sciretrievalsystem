import requests
import json, sys

class ESProcessor:

    def __init__(self, es_url, index_name):
        self.es_url = es_url
        self.index_name = index_name

    def search(self, query):
        url = self.es_url + "/" + self.index_name + "/_search"
        httpResp = requests.get(url,
                                data=json.dumps(query),
                                headers={"Content-Type" : "application/json"})
        results = json.loads(httpResp.text)
        searchHits = results["hits"]
        print("Num\tRelevance Score\t\t\tDocument Title")
        for idx, hit in enumerate(searchHits["hits"]):
            print("%s\t%s\t\t\t%s" %
                  (idx + 1, hit["_score"], hit["_source"]["title"]))
        return results

    def index(self, documentDict):
        bulkDocs = ""
        for id, document in documentDict.items():
            addCmd = {
                "delete" : {
                    "_index" : self.index_name,
                    "_id" : id
                },
                "index" : {
                    "_index" : self.index_name,
                    "_type" : self.type_name,
                    "_id" : id
                }
            }
            bulkDocs += json.dumps(addCmd) + "\n" + json.dumps(document) + "\n"
        resp = requests.post(self.es_url + "/_bulk",
                             data=bulkDocs,
                             headers={"Content-Type" : "application/x-ndjson"})

    def redefine_index(self, analysisSettings={}, mappingSettings={}, nos=1, nor=1):
        settings = {
            "settings": {
                "number_of_shards": nos,
                "number_of_replicas": nor,
                "index": {
                    "analysis" : analysisSettings
                }
            },
            # "mappings": {
            #     "properties": {
            #         "abstract": {
            #             "type": "text"
            #         },
            #         "aggregationType": {
            #             "type": "keyword"
            #         },
            #         "author": {
            #             "type": "text",
            #             "position_increment_gap": 100
            #         },
            #         "coverDate": {
            #             "type": "date"
            #         },
            #         "doi": {
            #             "type": "keyword"
            #         },
            #         "eid": {
            #             "type": "keyword"
            #         },
            #         "endingPage": {
            #             "type": "long"
            #         },
            #         "href": {
            #             "type": "text"
            #         },
            #         "id": {
            #             "type": "keyword"
            #         },
            #         "issn": {
            #             "type": "keyword"
            #         },
            #         "openaccess": {
            #             "type": "boolean"
            #         },
            #         "pageRange": {
            #             "type": "text"
            #         },
            #         "pii": {
            #             "type": "keyword"
            #         },
            #         "publicationName": {
            #             "type": "text"
            #         },
            #         "startingPage": {
            #             "type": "long"
            #         },
            #         "subject": {
            #             "type": "keyword"
            #         },
            #         "title": {
            #             "type": "text"
            #         },
            #         "volume": {
            #             "type": "text"
            #         }
            #     }
            # }
        }
        if mappingSettings:
            settings["mappings"] = mappingSettings

        resp = requests.delete(self.es_url + "/" + self.index_name)
        resp = requests.put(self.es_url + "/" + self.index_name,
                            data=json.dumps(settings),
                            headers={"Content-Type" : "application/json"})
        return resp



if __name__ == "__main__":
    es = ESProcessor("http://127.0.0.1:9200", "sci")
    query = {
        'query': {
            'multi_match': {
                'query': sys.argv[1],
                'fields': [
                    'title^10', 'abstract', 'subject^5'
                ]
            }
        }
    }
    es.search(query)
