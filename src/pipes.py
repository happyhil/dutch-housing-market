
import pandas as pd
import numpy as np
import re


def strip_int_column(dataf, columns):
    for c in columns:
        cvalues = list(dataf[c].values)
        cvalues = [re.sub('[^0-9]','', x) for x in cvalues]
        dataf[f'{c}_clean'] = [0 if y == '' else int(y) for y in cvalues]
    return dataf


def prepare_housing_dict(dicty):

    # merge dict into pandas frame
    housesdf = pd.DataFrame.from_dict(dicty, orient='index')

    # get city
    housesdf['city'] = housesdf['location'].str.split(',').str[1]
    housesdf['city'] = housesdf['city'].fillna('noaddress')

    # convert given columns to ints
    housesdf = strip_int_column(housesdf, ['price', 'meters'])

    # divide extreem high prices by 1000 to correct for dtype error in source
    housesdf.loc[lambda x: x['price_clean']>99999999, 'price_clean'] = housesdf['price_clean']/1000

    # calculate meter price on row level and replace failed calculation with 0
    housesdf['meter_price'] = housesdf['price_clean'] / housesdf['meters_clean']
    housesdf['meter_price'] = housesdf['meter_price'].replace([np.inf, -np.inf], 0)

    # filter on available houses only & houses with at least the field city filled
    housesdf = housesdf.loc[lambda x: x['status']=='available']
    housesdf = housesdf.loc[lambda x: x['location']!='noaddress']

    return housesdf


def housing_fact_dict(housesdf, area):

    # calculate metrics
    n_houses = housesdf['city'].count()
    average_price = round(housesdf.loc[lambda x: (x['price_clean']>0)]['price_clean'].mean(), 2)
    median_price = round(housesdf.loc[lambda x: (x['price_clean']>0)]['price_clean'].median(), 2)
    average_meters = round(housesdf.loc[lambda x: (x['meters_clean']>0)]['meters_clean'].mean(), 2)
    median_meters = round(housesdf.loc[lambda x: (x['meters_clean']>0)]['meters_clean'].median(), 2)
    average_meter_price = round(housesdf.loc[lambda x: (x['meter_price']>0)]['meter_price'].mean(), 2)
    median_meter_price = round(housesdf.loc[lambda x: (x['meter_price']>0)]['meter_price'].median(), 2)

    # create dict
    houses_dict = {
        area:
        {
            'number_available': int(n_houses),
            'price_mean': float(average_price),
            'price_median': float(median_price),
            'meters_mean': float(average_meters),
            'meters_median': float(median_meters),
            'meter_price_mean': float(average_meter_price),
            'meter_price_median': float(median_meter_price)
        }
    }

    return houses_dict


def build_full_dict(housesdf):

    # run totals
    overall_dict = housing_fact_dict(housesdf, area='The Netherlands')

    # run on cities
    cities = ['Amsterdam', 'Rotterdam', 'Utrecht', 'Hilversum', 'Amstelveen']
    cities_dicts = {}
    for city in cities:
        # filter on city
        city_housesdf = housesdf.loc[lambda x: x['city'].str.contains(city)]
        # create city sum
        sub_city_dict = housing_fact_dict(city_housesdf, area=city)
        # update cities
        cities_dicts.update(sub_city_dict)

    # merge dicts
    full_dict = {**overall_dict, **cities_dicts}

    return full_dict
