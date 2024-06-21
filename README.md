# scryfall-parse-bulk-data

The purpose of this is to parse the bulk data provided by scryfall into a smaller json file.

Scryfall offers a bulk data file, however for each MTG card there are many records. Each reprint of the card has it's own record. For my use cases this is not helpful. 

For example, if you search scryfall for "Aven of Enduring Hope", there are two prints. The original from Hour of Devastation says it's available on Paper/MTGO, but not Arena. The reprint from Amonkhet Remastered says it's available on Arena, but not paper/MTGO. My one record will say the card is available on all 3.

The script reads through the large file and creates another file (cardInfo.json) with one record with data for each card. I filter on each record that is either legal or banned in Commander. Scryfall has a large number of other records: tokens, un-sets, digital cards, etc. I filter out these. Not also it groups by name, so reskinned cards don't show up as a separate entry.

See a sample record below:
```
"Wall of Roots": {
  "sets": ["f08", "prm", "p30a", "arc", "wc98", "mir", "ima", "ncc", "tsb"], 
  "released_at": "1996-10-08", 
  "price_usd": 0.18,
  "legalitites": {"standard": "not_legal", "future": "not_legal", "historic": "not_legal", "timeless": "not_legal", "gladiator": "not_legal", "pioneer": "not_legal", "explorer": "not_legal", "modern": "legal", "legacy": "legal", "pauper": "legal", "vintage": "legal", "penny": "not_legal", "commander": "legal", "oathbreaker": "legal", "standardbrawl": "not_legal", "brawl": "not_legal", "alchemy": "not_legal", "paupercommander": "legal", "duel": "legal", "oldschool": "not_legal", "premodern": "legal", "predh": "legal"}, 
  "games": ["mtgo", "paper"]
}
```

"Sets" is a list of sets the card appears in.

"released_at" is the earliest released date for any print of the card.

"price_usd" is the lowest price scryfall has for any print of the card

"legalities" is the legality of each format. I thought about refactoring this but for now I just leave it exactly as Scryfall has it.

"games" is all the places it's available, (paper, arena and/or mtgo)



#NOTES:

This is designed to run on small hardware, either an Amazon AWS tiny image, or a Raspberry Pi, where memory/CPU are finite. We stream the download of default-cards.json, and the parsing of it (we don't load it all into memory at the same time). Otherwise we can have memory issues. That's why I use ijson. If you have a lot of memory, you can replace ijson with the standard json library, which should run faster. Parsing the large default-cards.json file can take 10 minutes in this way. Go get a coffee. You only need to do this once per set.

Note also, I do use the regular json library in other places. This is because for the smaller output file, json works fine (and ijson didn't, and I haven't checked why)

In the future I'd like to set this up so my script updates the cardInfo.json file on this repo every night, so you can always just download my file, and not have to generate your own
