import argparse
import subprocess
import re
import requests
from bs4 import BeautifulSoup
import episodeFilter

def req(query, all, quality):
    if all:
        res = requests.get("https://nyaa.si/?q="+query, headers={'User-Agent': 'puya-dl/1.0'})
    else:
        res = requests.get("https://nyaa.si/user/puyero?q="+query+"+"+quality, headers={'User-Agent': 'puya-dl/1.0'})
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
        p = re.compile(r'(?P<group>\[.*\])\s(?P<title>.*)\s-\s(?P<episode>\d+)')
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

def filter(items, title, episodes):
    filtered = []
        
    if episodes:
        episodes = episodeFilter.parseEpisodeFilter(episodes)
        for x in items:
            if x['title'] == title:
                try:
                    ep = int(x['episode'])
                    if ep in episodes:
                        filtered.append(x)
                except:
                    print("Couldn't parse episode number: ", x['episode'])
    else:
        for x in items:
            if x['title'] == title:
                filtered.append(x)
    return filtered

def download(items, noconfirm):
    first = 1
    for x in items[::-1]:
        if first == 1 and noconfirm == False:
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
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="puya.moe batch download tool")
    parser.add_argument('title', nargs='+', help="Exact title")
    parser.add_argument('-q', '--quality', dest="quality", help="Quality (usually only 720p and 1080p is available)", default="1080p")
    parser.add_argument('-e', '--episodes', dest="episodes", help="Specify episodes to download", required=False)
    parser.add_argument('--dryrun', action='store_true', dest="dryrun", help="Dry run (only for development)")
    parser.add_argument('--quiet', '--noconfirm', action='store_true', dest="noconfirm", help="Don't ask for confirmation")
    parser.add_argument('--all', action='store_true', dest="all", help="Search for all releases (not only puya) (experimental)")

    args = parser.parse_args()
    query = ' '.join(args.title)

    if args.dryrun:
        exit()

    items = req(query, args.all, args.quality)
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
            filtered = filter(items, titles[output], args.episodes)
            download(filtered, args.noconfirm)
    else:
        filtered = filter(items, titles[0], args.episodes)
        download(filtered, args.noconfirm)

    print("\033[93mFinished.\033[0m")
