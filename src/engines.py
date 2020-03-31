
import requests
import json
from os import path
from bs4 import BeautifulSoup
from datetime import datetime


def scrape_jaap(target):

    today = datetime.now().strftime('%Y_%m_%d')

    response = requests.get(target.format(1))
    soup = BeautifulSoup(response.content, 'html.parser')
    number_of_pages = int(soup.select('.navigation-buttons span')[0].text.split()[-1])

    count = 0
    full_houses_dict = {}
    for n_page in range(1, number_of_pages+1):

        response = requests.get(target.format(n_page))
        soup = BeautifulSoup(response.content, 'html.parser')
        houses = soup.select('.property')

        for h in houses:

            # location
            try:
                location = h.select('.property-address-zipcity')[0].text
            except:
                location = 'noaddress'

            # price
            try:
                price = h.select('.property-price')[0].text
            except:
                price = 'noprice'

            # meters
            try:
                meters = houses[0].select('.property-feature')[2].text
            except:
                meters = 'nometers'


            # status
            try:
                status = h.select('.property-photo span')[0].text
            except:
                status = 'available'

            house_dict = {
                       count:
                            {
                           'location': location,
                           'price': price,
                           'meters': meters,
                           'status': status
                            }
                        }
            full_houses_dict.update(house_dict)
            count +=1

        # save temp result
        outfile = f'housing_data_{today}.json'
        outdir = f'data/raw/{outfile}'
        if not path.isfile(outdir):
            with open(outdir, 'w') as outstream:
                json.dump(full_houses_dict, outstream, indent=2)
        else:
            with open(outdir, 'r') as instream:
                current_full_houses_dict = json.load(instream)
            current_full_houses_dict.update(full_houses_dict)
            with open(outdir, 'w') as outstream:
                json.dump(current_full_houses_dict, outstream, indent=2)
