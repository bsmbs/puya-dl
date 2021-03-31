from puyadl.scraper import Scraper
from puyadl.gui import initialize
import sys
import argparse

def download(scraper, noconfirm):
    if noconfirm:
        scraper.downloadFirstItem()
        scraper.download()
    else:
        print("\033[93mYour BitTorrent client should open with the first file. Please specify a directory so your client remembers it. Type 'cancel' if you want to abort or anything else to continue.\033[0m")
        scraper.downloadFirstItem()
        a = input("(cancel/continue)> ").lower()
        if a == 'cancel':
            print("Cancel")
        else:
            print("\033[93mContinuing.\033[0m")
            scraper.download()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="puyadl", description="puya.moe batch download tool")
    parser.add_argument('title', nargs='+', help="Exact title")
    parser.add_argument('-q', '--quality', dest="quality", help="Quality (usually only 720p and 1080p is available)", default="1080p")
    parser.add_argument('-e', '--episodes', dest="episodes", help="Specify episodes to download", required=False)
    parser.add_argument('--dryrun', action='store_true', dest="dryrun", help="Dry run (only for development)")
    parser.add_argument('--quiet', '--noconfirm', action='store_true', dest="noconfirm", help="Don't ask for confirmation")
    parser.add_argument('--all', action='store_true', dest="all", help="Search for all releases (not only puya) (experimental)")

    if len(sys.argv) > 1: # Arguments provided, CLI mode
        args = parser.parse_args()
        query = ' '.join(args.title)

        if args.dryrun:
            exit()
        
        scraper = Scraper(args)
        scraper.request(query)
        titles = scraper.list_titles()

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

                scraper.filter(titles[output])
                download(scraper, args.noconfirm)    
        else:
            scraper.filter(titles[0])
            download(scraper, args.noconfirm)

        print("\033[93mFinished.\033[0m")

    else: # Arguments not provided, initialize gui
        print("Initializing Qt6 gui")
        initialize()