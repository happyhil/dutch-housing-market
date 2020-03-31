#!/usr/bin/env python

from src.engines import scrape_jaap

def main():

    # scrape_jaap('https://www.jaap.nl/koophuizen/p{}')
    scrape_jaap('https://www.jaap.nl/koophuizen/noord+brabant/midden-noord-brabant/baarle-nassau/p{}')

if __name__ == '__main__':
    main()
