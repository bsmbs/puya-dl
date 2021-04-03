from puyadl.episode_parser import parseEpisodeFilter
import argparse
import subprocess
import re
import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self, args):
        self.args = args

    def request(self, query):
        if self.args.all:
            res = requests.get("https://nyaa.si/?q="+query, headers={'User-Agent': 'puya-dl/1.0'})
        else:
            res = requests.get("https://nyaa.si/user/puyero?q="+query+"+"+self.args.quality, headers={'User-Agent': 'puya-dl/1.0'})
        parsed = BeautifulSoup(res.content, 'html.parser')

        self.items = []

        results = parsed.find_all('tr') # Find every row
        if len(results) == 0:
            print("No results found.")
            return
                    
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
            self.items.append(ep)

        # return items

    def list_titles(self):
        unq_list = []
        for x in self.items:
            if x['title'] not in unq_list:
                unq_list.append(x['title'])

        return unq_list

    def filter(self, title):
        filtered = []
            
        if self.args.episodes:
            episodes = parseEpisodeFilter(self.args.episodes)
            for x in self.items:
                if x['title'] == title:
                    try:
                        ep = int(x['episode'])
                        if ep in episodes:
                            filtered.append(x)
                    except:
                        print("Couldn't parse episode number: ", x['episode'])
        else:
            for x in self.items:
                if x['title'] == title:
                    filtered.append(x)

        self.items = filtered
    
    def downloadFirstItem(self):
        subprocess.run(['xdg-open', self.items[-1]['magnet']], stderr=subprocess.DEVNULL)

    def download(self):
        for x in self.items[::-1][1:]:
            subprocess.run(['xdg-open', x['magnet']], stderr=subprocess.DEVNULL)