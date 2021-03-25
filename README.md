# puya-dl

Short Python script for batch downloading PuyaSubs releases

Doesn't work with shows longer than 75 episodes because I'm too lazy to implement it properly. Should work tho

## Requirements
* Python... a new version I guess
* `xdg-open` (doesn't work on Windows for now)
* a BitTorrent client

## Install
Just clone this repository, do `pip install -r requirements.txt`. You can do this venv thing if you want.

## Usage
`python main.py "search query"`

Default quality is 1080p. If you want to specify a different one, use -q, for example -q 720p.