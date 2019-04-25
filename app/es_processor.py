import requests
import json

class ESProcessor:

    def __init__(self, es_url, index_name):
        self.es_url = es_url
        self.index_name = index_name

    def search(self, query):
        url = self.es_url + "/" + self.index_name + "/document/_search"
        httpResp = requests.get(url,
                                data=json.dumps(query),
                                headers={"Content-Type" : "application/json"})
        results = json.loads(httpResp.text)
        searchHits = results["hits"]
        print("Num\tRelevance Score\t\t\tDocument Title")
        for idx, hit in enumerate(searchHits["hits"]):
            print("%s\t%s\t\t\t%s" %
                  (idx + 1, hit["_score"], hit["_source"]["dc:title"]))
        # return results


    def reindex(self, analysisSettings={}, mappingSettings={}, nos=1):
        settings = {
            "settings" : {
                "number_of_shards" : nos,
                "index" : {
                    "analysis" : analysisSettings
                }
            }
        }
        if mappingSettings:
            settings["mappings"] = mappingSettings

        resp = requests.delete(self.es_url + "/" + self.index_name)
        resp = requests.put(self.es_url + "/" + self.index_name,
                            data=json.dumps(settings),
                            headers={"Content-Type" : "application/json"})


    def extract(self, filename=""):
        try:
            f = open(filename, "rb")
        except IOError:
            print("Error: No such file, or failed to open file.")
        else:
            return json.loads(f.read())
            fh.close()
