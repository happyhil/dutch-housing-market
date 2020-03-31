#!/usr/bin/env python

from src.engines import scrape_jaap

def main():

    print(f'Running {path.basename(__file__)}..')

    # execute scraper on given url
    scrape_jaap('https://www.jaap.nl/koophuizen/p{}')

if __name__ == '__main__':
    main()
