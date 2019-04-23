import requests
import json

class ESProcessor:

    def __init__(self, es_url, index_name):
        self.es_url = es_url
        self.index_name = index_names

    def search(self, query):
        url = self.es_url + "/" + self.index_name + "/document/_search"
        httpResp = requests.get(url,
                                data=json.dumps(query),
                                headers={"Content-Type" : "application/json"})
        searchHits = json.loads(httpResp.text)["hits"]
        print("Num\tRelevance Score\t\t\tDocument Title")
        for idx, hit in enumerate(searchHits["hits"]):
            print("%s\t%s\t\t\t%s" %
                  (idx + 1, hit["_score"], hit["_source"]["dc:title"]))


    def reindex(self, analysisSettings={}, mappingSettings={}, dict={}):
        settings = {
            "settings" : {
                "number_of_shards" : 2,
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
        bulkDocs = ""
        documentDict = dict
        for id, document in documentDict.items():
            addCmd = {
                "index" : {
                    "_index" : "sci",
                    "_type" : "document",
                    "_id" : document["pii"]
                }
            }
            bulkDocs += json.dumps(addCmd) + "\n" + json.dumps(document) + "\n"
        resp = requests.post(self.es_url + "/_bulk",
                             data=bulkDocs,
                             headers={"Content-Type" : "application/x-ndjson"})

    def extract(self, filename=""):
        try:
            f = open(filename, "rb")
        except IOError:
            print("Error: No such file, or failed to open file.")
        else:
            return json.loads(f.read())
            fh.close()
