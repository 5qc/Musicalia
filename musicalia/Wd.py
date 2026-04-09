from datetime import datetime
from ._headers import headers

import requests

class Wd:
    def __init__(self, qid: str):
        r = requests.get(f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json", headers=headers)
        
        self.qid = qid
        self.json = r.json()["entities"][qid]
    
    def label(self, lang: str):
        if ("mul" not in self.json["labels"]) and (lang not in self.json["labels"]):
            return None
        if lang not in self.json["labels"]:
            return self.json["labels"]["mul"]["value"]
        else:
            return self.json["labels"][lang]["value"]
    
    def claim(self, property: str, value: str = "all"):
        if property not in self.json["claims"]: return []
        
        dx = self.json["claims"][property]
        l = []
        
        for x in dx:
            if (value == "one") and (x["rank"] == "deprecated"): continue
            if (value == "one") and (x["rank"] == "preferred"): l = []
            
            snaktype = x["mainsnak"]["datatype"]
            match snaktype:
                case "wikibase-item":
                    l.append(x["mainsnak"]["datavalue"]["value"]["id"])
                case "time":
                    time = datetime.strptime(x["mainsnak"]["datavalue"]["value"]["time"], "+%Y-%m-%dT%H:%M:%SZ")
                    precision = x["mainsnak"]["datavalue"]["value"]["precision"]
                    
                    tx = ""
                    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                    
                    match precision:
                        case 11: tx = f"{time.day} {month[time.month-1]} {time.year}" # day
                        case 10: tx = f"{month[time.month-1]} {time.year}" # month
                        case 9: tx = f"{time.year}" # year
                        case 8: "" # decade
                        case 7: "" # century
                        case 6: "" # millennium
                        case 5: "" # 10,000 years
                        case 4: "" # 100,000 years
                        case 3: "" # million years
                        case 2: "" # ten million years
                        case 1: "" # hundred million years
                        case 0: "" # billion years
                        
                    l.append(tx)
                case "external-id":
                    string = Wd("P7067").claim("P1630", "one")
                    rpl = x["mainsnak"]["datavalue"]["value"]
                    
                    l.append( string.replace("$1", rpl) )
                case "string":
                    l.append(x["mainsnak"]["datavalue"]["value"])
            
            if (value == "one") and (x["rank"] == "preferred"): break

        if value == "one": return l[0]
        else: return l
    
    def sitelink(self, code: str):
        if code not in self.json["sitelinks"]:
            return None
        else:
            return self.json["sitelinks"][code]["url"].replace("https://en.wikipedia.org/wiki/", "")