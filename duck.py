#!/usr/bin/env python

import json
import random
import argparse
import requests
from discord import SyncWebhook

def getArgs():
    args = argparse.ArgumentParser(prog="Duck Daily")
    args.add_argument("-a", "--apikeys")
    return args.parse_args()

def getApiKey(apifile):
    with open(apifile, "r") as file:
        return json.load(file)
    
def findduck(gifhyApiKey):
    url = "https://api.giphy.com/v1/gifs/search?api_key=" + gifhyApiKey +"&q=duck&limit=5&offset=" + str(random.randint(0, 256)) + "&rating=g&lang=en&bundle=messaging_non_clips"
    r = requests.get(url)
    return r.json()

def postduck(duckurl,discordwebhook):
    webhook = SyncWebhook.from_url(discordwebhook)
    webhook.send(duckurl)

def turnArrayIntoString(array):
    returnstring = ""
    for item in array:
        returnstring = item + "\n" + returnstring
    return returnstring

if __name__ == '__main__':
    args = getArgs()
    keys = getApiKey(args.apikeys)
    gifhyApiKey = keys["gifhy"]
    discord = keys["discord"]

    duckgifs = findduck(gifhyApiKey)
    duckGifUrls = []
    for duck in duckgifs["data"]:
        duckGifUrls.append(duck["embed_url"])
    duckstring =  turnArrayIntoString(duckGifUrls)

    print(duckstring)

    postduck(duckstring,discord)