from dotenv import load_dotenv
import os
# import requests, json

load_dotenv(os.path.join("../", '.env'))

# def reindex(analysisSettings={}, mappingSettings={}, nos=1):
#     settings = {
#         "settings" : {
#             "number_of_shards" : nos,
#             "index" : {
#                 "analysis" : analysisSettings
#             }
#         }
#     }
#     if mappingSettings:
#         settings["mappings"] = mappingSettings
#
#     resp = requests.delete("http://localhost:9200/sci")
#     resp = requests.put("http://localhost:9200/sci",
#                         data=json.dumps(settings),
#                         headers={"Content-Type" : "application/json"})
#
# reindex()
