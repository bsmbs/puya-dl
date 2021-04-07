# puya-dl

Simple app written in Python for batch downloading PuyaSubs releases. It includes an 'All releases' option so you can use it for HorribleSubs as well.

Doesn't work with shows longer than 75 episodes because I'm too lazy to implement it properly.

## Requirements
* Python 3... a new version I guess
* Qt 6
* a BitTorrent client

## Install
```sh
> pip install puya-dl
```

or just clone this repository and do `python setup.py install`

## Usage
### GUI
The command without any arguments fires up the GUI. If you want to see CLI help, use -h.

```sh
> python -m puyadl
```
### CLI
```sh
> python -m puyadl "search query"
```

```
usage: puyadl [-h] [-q QUALITY] [-e EPISODES] [--dryrun] [--quiet] [--all] title [title ...]

puya.moe batch download tool

positional arguments:
  title                 Exact title

optional arguments:
  -h, --help            show this help message and exit
  -q QUALITY, --quality QUALITY
                        Quality (usually only 720p and 1080p is available)
  -e EPISODES, --episodes EPISODES
                        Specify episodes to download
  --dryrun              Dry run (only for development)
  --quiet, --noconfirm  Don't ask for confirmation
  --all                 Search for all releases (not only puya) (experimental)
```

Default quality is 1080p. If you want to specify a different one, use -q, for example -q 720p.

### Episode filters
By default, puya-dl selects and downloads all episodes. When -e argument is passed, only selected episodes are downloaded. Just enter episode number to select an episode. You can also use ranges like `1-3`. Seperate filters with a single comma (,).

For example, `python -m puyadl title -e 1-2,5-6,10` will select episodes 1, 2, 5, 6 and 10.