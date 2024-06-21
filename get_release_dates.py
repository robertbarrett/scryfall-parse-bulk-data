from datetime import datetime
import json


f = open('cardInfo.json')

data = json.load(f)
for name in data.keys():
  print(name+"|"+data[name]["released_at"])
