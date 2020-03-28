#!/usr/bin/env python

from src.engines import scrape_jaap

def main():

    scrape_jaap('https://www.jaap.nl/koophuizen/p{}')

if __name__ == '__main__':
    main()
