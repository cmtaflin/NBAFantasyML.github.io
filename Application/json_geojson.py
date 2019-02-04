# This file is designed as a function that other application can call.  It will take in a pandas dataframe and give you a geojson

import pandas as pd
import json

# function to convert a dataframe to a geojson.  Thank you to Geoff Boeing for the online documentation that was used.
def to_geojson(df, properties, lat='LATITUDE', lon='LONGITUDE'):
    
    # Turn a dataframe containing point data into a geojson formatted python dictionary 
    # df : the dataframe to convert to geojson
    # properties : a list of columns in the dataframe to turn into geojson feature properties
    # lat : the name of the column in the dataframe that contains latitude data (default is based on database used originally)
    # lon : the name of the column in the dataframe that contains longitude data (default is based on database used originally)

    # create python dict to contain geojson data, using geojson format. start with feature type...
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        #create the feature part to fill in (using the feature part of dict above)
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        #fill in coordinates (lat/long)
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        
        # use the command below if you want ALL columns to be included in the geojson.  Otherwise change properties variable.
        properties = list(df.columns.values)

        #for each column in dataframe, get the value and add to properties. Loop within the overall loop of rows.
        for prop in properties:
            feature['properties'][prop] = row[prop]
            
        # add this feature from the dataframe row to the list of features in geojson
        geojson['features'].append(feature)
        
            
    return geojson

