#!/usr/bin/env python


import json
from os import path
from datetime import datetime
from src import pipes


def main():

    print(f'Running {path.basename(__file__)}..')

    # define today
    # today = datetime.now().strftime('%Y_%m_%d')
    today = '2020_03_28'

    # read in way data
    with open(f'data/raw/housing_data_{today}.json', 'r') as stream:
        housesdict = json.load(stream)

    # prep data for calculations
    housesdf = pipes.prepare_housing_dict(housesdict)

    # run calculations and build the dict
    full_dict = pipes.build_full_dict(housesdf)

    # create the output dict
    output_dict = {
        today: {
            'version': 0.1,
            'housing_facts': full_dict
        }
    }

    # check if current file exists
    if path.isfile('data/shots/housing_market_shots.json'):
        # append data to existing json
        with open('data/shots/housing_market_shots.json', 'r') as rshotsstream:
            shots = json.load(rshotsstream)
        newshots = {**shots, **output_dict}
        with open('data/shots/housing_market_shots.json', 'w') as wshotstream:
            json.dump(newshots, wshotstream, indent=2)
    else:
        # write new json
        with open('data/shots/housing_market_shots.json', 'w') as wshotstream:
            json.dump(output_dict, wshotstream, indent=2)

if __name__ == '__main__':
    main()
