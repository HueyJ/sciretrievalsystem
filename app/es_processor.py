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
