# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:09:38 2017

@author: adivt
Code adapted from: https://willgeary.github.io/GPXto3D/
"""

import pandas as pd
import numpy as np
import gpxpy
import json



def parse_gpx(gpx_input_file):
    
    lats = []
    lons = []
    names = []
    desc = []
    times = []
    print('\n\n')
    for waypoint in gpx.waypoints:
        lats.append(waypoint.latitude)
        lons.append(waypoint.longitude)
        names.append(waypoint.name)
        desc.append(waypoint.description)
        times.append(waypoint.time)
                   
    output = pd.DataFrame()
    output['latitude'] = lats
    output['longitude'] = lons
    output['names'] = names
    output['desc'] = desc
    output['time'] = times
    
    return output

def create_czml_path(df_input, relative_elevation = False):
    results = []
    
    timestep = 0
    
    for i in df_input.index:
        results.append(timestep)
        results.append(df_input.longitude.ix[i])
        results.append(df_input.latitude.ix[i])
        duration = 300 #hardcoded to 300secs because our gpx lacks duration
        timestep += duration
        
    return results

def point_with_trailing_path(df_input, time_multiplier = 1000):
    
    # Store output in array
    czml_output = []

    # Define global variables
    global_id = "document"
    global_name = "Visualizing GPX Data in Cesium"
    global_version = "1.0"
    global_author = "Aditya Gune"
    global_time = str(min(df_input['time'])).replace(" ", "T").replace(".000", "Z")
    global_endtime = str(max(df_input['time'])).replace(" ", "T").replace(".100", "Z")
    global_availability = global_time + "/" + global_endtime    
    
    # Create packet with global variables
    global_element = {
        "id" : global_id,
        "name" : global_name,
        "version" : global_version,
        "author": global_author,
        "clock": {
            "interval": global_availability,
            "currentTime": global_time,
            "multiplier": time_multiplier
        }
    }
    
    # Append global packet to output
    czml_output.append(global_element)
    
    # Define path variables
    path_id = "path"
    path_time = str(min(df_input['time'])).replace(" ", "T").replace(".000", "Z")
    path_endtime = str(max(df_input['time'])).replace(" ", "T").replace(".100", "Z")
    path_availability = path_time + "/" + path_endtime
    
    # Create path object
    path_object = {
            "id": path_id,

            "availability": path_availability,

            "position": {
                "epoch": path_time,
                "cartographicDegrees": create_czml_path(df, relative_elevation=False)
            },

            "path" : {
                "material" : {
                    "polylineOutline" : {
                        "color" : {
                            "rgba" : [255,255,255, 200]
                        },
                        "outlineColor" : {
                            "rgba" : [0,173,253, 200]
                        },
                        "outlineWidth" : 5
                    }
                },
                "width" : 6,
                "leadTime" : 0,
                "trailTime" : 100000,
                "resolution" : 5
            }
        }

    # Append path element to output
    czml_output.append(path_object)
        
    # Define point variable
    point_id = "Point"
    point_time = str(min(df_input['time'])).replace(" ", "T").replace(".000", "Z")
    point_endtime = str(min(df_input['time'])).replace(" ", "T").replace(".100", "Z")
    point_availability = point_time + "/" + point_endtime
    
    point_object = {
            "id": point_id,

            "availability": point_availability,

            "position": {
                "epoch": point_time,
                "cartographicDegrees": create_czml_path(df, relative_elevation=True)
            },

            "point": {
                "color": {
                    "rgba": [255, 255, 255, 255]
                },
                "outlineColor": {
                    "rgba": [0,173,253, 255]
                },
                "outlineWidth":6,
                "pixelSize":8,
                "heightReference" : "RELATIVE_TO_GROUND"
            }   
        }

    czml_output.append(point_object)
    
    return czml_output

gpx_file = open('./St_Louis_Zoo_sample.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
df = parse_gpx(gpx)
df.head()
czml = create_czml_path(df)
print(czml)
czml_output = point_with_trailing_path(df)

with open('./zoo.czml', 'w') as outfile:
    json.dump(czml_output, outfile)