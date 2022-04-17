
import json

import requests

def anime(query):

    r = requests.get("https://animepahe.com/api?m=search&q="+query)
    results = json.loads(r.text)

    for idx, i in enumerate(results["data"]):
        poster = (results["data"][idx]["poster"])
        title = (results["data"][idx]["title"])
        type = (results["data"][idx]["type"])
        episodes = (results["data"][idx]["episodes"])
        score = (results["data"][idx]["score"])
        status = (results["data"][idx]["status"])
        link = 'https://animepahe.com/anime/'+(results["data"][idx]["session"])

        li = []

        dc = {
            "poster": poster,
            "title": title,
            "type": type,
            "episodes": episodes,
            "score": score,
            "status": status,
            "link": link
        }

        li.append(dc)

        for i in li:
            ko = i
            yield(ko)

def anime_total(query):
    r = requests.get("https://animepahe.com/api?m=search&q="+query)
    results = json.loads(r.text)

    total = results["total"]
    return total




