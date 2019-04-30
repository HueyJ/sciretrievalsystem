import requests, json


def __reindex(analysisSettings={}, mappingSettings={}, nos=1):
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

    resp = requests.delete("http://127.0.0.1:9200" + "/" + "sci")
    resp = requests.put("http://127.0.0.1:9200" + "/" + "sci",
                        data=json.dumps(settings),
                        headers={"Content-Type" : "application/json"})
