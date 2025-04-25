#!/usr/bin/env python

import json
import random
import argparse
import requests

def getArgs():
    args = argparse.ArgumentParser(prog="Duck Daily")
    args.add_argument("-a", "--apikeys")
    args.add_argument("-g", "--google", help="Send message webhook formatted for google chat not discord.")
    args.add_argument("--showoff",action="store_true", help="inclue github link in post")
    return args.parse_args()

def getApiKey(apifile):
    with open(apifile, "r") as file:
        return json.load(file)
    
def findduck(gifhyApiKey):
    url = "https://api.giphy.com/v1/gifs/search?api_key=" + gifhyApiKey +"&q=duck&limit=5&offset=" + str(random.randint(0, 256)) + "&rating=g&lang=en&bundle=messaging_non_clips"
    r = requests.get(url)
    return r.json()

def postduckdiscord(message,discordwebhook):
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    data = {
        "content" : message,
    }
    return requests.post(url=discordwebhook, headers=headers, json = data)

def postduckgoogle(message,webhook):
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    data = {
        "text" : message,
    }
    return requests.post(url=webhook, headers=headers, json = data)

def turnArrayIntoString(array):
    returnstring = ""
    for item in array:
        returnstring = item + "\n" + returnstring
    return returnstring

if __name__ == '__main__':
    args = getArgs()
    keys = getApiKey(args.apikeys)
    gifhyApiKey = keys["gifhy"]
    webhook = keys["webhook"]

    duckgifs = findduck(gifhyApiKey)
    duckGifUrls = []
    for duck in duckgifs["data"]:
        duckGifUrls.append(duck["embed_url"])
    duckstring =  turnArrayIntoString(duckGifUrls)

    if args.showoff:
        duckstring = duckstring + "\nhttps://github.com/dylanbuel/duckaday"

    print(duckstring)

    if args.google:
        postduckgoogle(duckstring,webhook)
    else:
        postduckdiscord(duckstring,webhook)