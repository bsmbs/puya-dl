import argparse
import subprocess
import re
import requests
from bs4 import BeautifulSoup

def req(query, q):
    res = requests.get("https://nyaa.si/user/puyero?q="+query+"+"+q, headers={'User-Agent': 'puya-dl/1.0'})
    parsed = BeautifulSoup(res.content, 'html.parser')

    items = []

    results = parsed.find_all('tr') # Find every row
    if len(results) == 0:
        print("No results found.")
        exit()
    
    for result in results[1:]:
        links = result.select('td a')
        if "comments" in links[1]['href']:
            title = links[2]['title']
        else:
            title = links[1]['title'] # Title
        
        print(title)
        p = re.compile(r'(\[PuyaSubs!\])\s(?P<title>.*)\s-\s(?P<episode>\d+)')
        m = p.search(title)
        if not m:
            print("No match")
            continue
        ep = {
            "title": m.group('title'),
            "episode": m.group('episode'),
            "magnet": links[-1]['href']
        }
        items.append(ep)
    return items

def list_titles(items):
    unq_list = []
    for x in items:
        if x['title'] not in unq_list:
            unq_list.append(x['title'])

    return unq_list

def download(title, items):
    first = 1
    for x in items[::-1]:
        if x['title'] == title:
            if first == 1:
                print("\033[93mYour BitTorrent client should open with the first file. Please specify a directory so your client remembers it. Type 'cancel' if you want to abort or anything else to continue.\033[0m")
                subprocess.run(['xdg-open', x['magnet']], stderr=subprocess.DEVNULL)
                a = input("(cancel/continue)> ").lower()
                if a == 'cancel':
                    print("Cancel")
                    break
                else:
                    first = 0
                    print("\033[93mContinuing.\033[0m")
                    continue
            else:
                subprocess.run(['xdg-open', x['magnet']], stderr=subprocess.DEVNULL)

# ARGPARSE
parser = argparse.ArgumentParser(description="puya.moe batch download tool")
parser.add_argument('title', metavar="Title", nargs='+', help="Exact title")
parser.add_argument('-q', '--quality', dest="quality", help="Quality (usually only 720p and 1080p is available)", default="1080p")
args = parser.parse_args()

query = ' '.join(args.title)
q = args.quality

items = req(query, q)
titles = list_titles(items)

if len(titles) > 1:
    print("Multiple titles found. Please select which one you want to download")
    for i, title in enumerate(titles):
        print(i, ")", title)
    output = int(input("Number > "))
    if output > len(titles) or output < 0:
        print("Incorrect number. Exiting")
        exit(0)
    else:
        print("Selected", titles[output])
        download(titles[output], items)
else:
    download(titles[0], items)

print("\033[93mFinished.\033[0m")
