import requests
import ijson
from datetime import datetime
import json


def getLowestDate(dateStrList):
  lowestDate="9999-12-12"
  for dateStr in dateStrList:
    try:
      if datetime.strptime(dateStr, "%Y-%m-%d")<datetime.strptime(lowestDate, "%Y-%m-%d"):
        lowestDate=dateStr
    except Exception as e:
      print(e)
      pass
  return lowestDate

def getLowestPrice(priceList):
  lowestPrice=9999999999.9
  for price in priceList:
    try:
      lowestPrice=min(lowestPrice,float(price))
    except Exception as e:
      #print(e)
      pass
  return lowestPrice

def getArtListFromCardData(card):
  imageList=[]
  if "image_uris" in card:
    imageList.append(card["image_uris"]["png"])
  else:
    for face in card["card_faces"]:
      imageList.append(face["image_uris"]["png"])
  return imageList

#request_url = requests.get('https://api.scryfall.com/bulk-data')
#request_data = requests.get(request_url.json()['data'][2]['download_uri'], stream=True)
#with open("default-cards.json", mode="wb") as file:
#  for chunk in request_data.iter_content(chunk_size=10*1024):
#    file.write(chunk)


nameDict={}
with open("default-cards.json","rb") as f:
  for record in ijson.items(f, "item"):
    if record["legalities"]["commander"] in ["legal", "banned"]:
      cardName=record["name"]
      cardSet=record["set"]
      cardReleased=record["released_at"]
      cardPrice=getLowestPrice([record["prices"]["usd"],record["prices"]["usd_foil"],record["prices"]["usd_etched"]])
      cardLegalities=record["legalities"]
      cardGames=record["games"]
      cardCollectorNumber=record["collector_number"]
      cardArtList=getArtListFromCardData(record)
      cardArtDict={cardSet: {"collector_number": cardCollectorNumber, "image_uris": cardArtList}}

      if record["name"] not in nameDict.keys():
        nameDict[cardName]={"sets": [record["set"]], "released_at": cardReleased, "price_usd": cardPrice, "legalitites": cardLegalities, "games": cardGames}
      else:
        if cardSet not in nameDict[record["name"]]["sets"]:
          nameDict[record["name"]]["sets"].append(cardSet)
        nameDict[record["name"]]["released_at"]=getLowestDate([record["released_at"], nameDict[record["name"]]["released_at"]])
        nameDict[record["name"]]["price_usd"]=getLowestPrice([record["prices"]["usd"],record["prices"]["usd_foil"],record["prices"]["usd_etched"], nameDict[record["name"]]["price_usd"]])
        nameDict[record["name"]]["games"]=list(set(record["games"]+nameDict[record["name"]]["games"]))

with open("cardInfo.json","w") as f:
  json.dump(nameDict,f)
