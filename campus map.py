"""
Created on Fri Oct 29 22:38:55 2021

@author: abigailkennedy
"""

import streamlit as st
import pandas as pd
import pydeck as pdk

class Node:
    """
    A class containing the initializer for node object
    """
    def __init__(self, location, lat, lon, time, left, right):
        """
        Location: The name of the location
        Lat: The location's latitude
        Lon: The location's longitude
        Time: How long it takes to reach this location from the parent node

        Returns
        -------
        None

        """
        self.location = location
        self.lat = lat
        self.lon= lon
        self.time = time
        self.left = left
        self.right = right
        
        
def path(destination):
    """
    Calls for a tree in the form of an array to be created, then calls a search
    for the shortest path to a destination.

    Returns
    -------
    None
    """
    #Create the array/tree
    array = treeBuilder()
    
    #Return the path
    search(array, destination)
    

def treeBuilder():
    """
    Takes comma deliminated text (used in place of a csv file due to technical 
    difficulties) and creates an array of nodes containing information on a
    location's name, latitude, longitude, time between locations, and connecting
    locations.

    Returns
    -------
    Locations: An array containing location data

    """
    #location,lat,lon,time,left,right
    txt = "Walker Ave (S),39.259030,-76.71479,0,Lot 8 - Smoking Area,None,\
    Lot 8 - Smoking Area,39.256832,-76.714385,180,PAHB (E),Upper Walkway - FAB Staircase,\
    PAHB (E),39.255066,-76.714639,184,Upper Walkway - ENGR/ITE Staircase,None,\
    Upper Walkway - FAB Staircase,39.255615,-76.713958,116,Upper Walkway - FAB/ENGR Staircase,None,\
    Upper Walkway - ENGR/ITE Staircase,39.254311,-76.714547,53,None,None,\
    Upper Walkway - FAB/ENGR Staircase,39.254982,-76.714275,53,None,Upper Walkway - ENGR/ITE Staircase,\
    Upper Walkway - ENGR/ITE Staircase,39.254311,-76.714547,56,None,None,\
    Staircase - FAB/ENGR,39.254847,-76.713833,27,None,Center Walkway - FAB/MEYR/UC/ENGR,Staircase - FAB/ENGR,\
    Center Walkway - FAB/MEYR/UC/ENGR,39.254702,-76.713359,36,None,None"
    
    lines = txt.split(',')
    locations = []
    i = 0
    while (i<54):
        location = lines[i]
        lat = lines[i+1]        
        lon = lines[i+2]        
        time = lines[i+3]        
        left = lines[i+4]        
        right = lines[i+5]
        node = Node(location, lat, lon, time, left, right)
        locations.append(node)
        i=i+6;
    
    return locations   

    
def search(array, destination):
    """
    A search to find the fastest route to class
    
    Array: An array of our locations
    Destination: Where we would like to end up
    
    Returns
    -------
    Path: The fastest route to class
    """

    #Identify the end of the line
    i = 0
    result = 0;
    for i in range(len(array)-1):
        if array[i].location.strip() == destination.strip():
            result = i
            break
        else:
            i=i+1
                 
    #Now reverse engineer the path and time
    time = 0 #variable to add time to in seconds
    path = [array[result].location] #array to add locations into
    
    var = True
    j = 0
    while var == True:
        for j in range(len(array)-1):
            if array[i].location.strip() == array[j].left.strip() or \
            array[i].location.strip() == array[j].right.strip():
                if array[j].location.strip() not in path:
                    path.insert(0, array[j].location.strip() )
                    time += int(array[i].time)
                    i = j
                    break
            else:
                j=j+1
        if array[j].location.strip() == array[0].location.strip():
            #path.insert(0, array[0].location.strip() )
            #time += int(array[0].time)
            var = False
    
    solution(path, time)
    
def solution(path, time):
    """
    Generates the final map with the solution for the quickest route

    Returns
    -------
    None
    """
    
    st.write('The fastest path is: \n', path)
    
    #Convert time into minutes
    m,s = divmod(time, 60)
    st.write('It will take ', m, ' minutes and ', s, ' seconds to reach your destination')


def createLatLonDict():
    """
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    Lat: The latitude of each location
    Lon: The longitude of each location
    Name: The name of each location
    
    Returns
    -------
    The dictionary created from the data
    """
    dictionary = {'lat': [39.259030, 39.256832, 39.255615, 39.254982, 39.254847,
                          39.254311, 39.255066, 39.254702],
                  'lon': [-76.71479, -76.714385, -76.713958, -76.714275, -76.713833,
                          -76.714547, -76.714639, -76.713359],
                  'name': ['Walker Ave (S)', 'Lot 8 - Smoking Area',
                           'Upper Walkway - FAB Staircase',
                           'Upper Walkway - FAB/ENGR Staircase',
                           'Staircase - FAB/ENGR', 
                           'Upper Walkway - ENGR/ITE Staircase',
                           'PAHB (E)', 'Center Walkway - FAB/MEYR/UC/ENGR']}
    df = pd.DataFrame(data=dictionary)
    return df


def createPathDict():
    """
    Lat: The latitude of the starting location
    Lon: The longitude of the starting location
    Lat2: The latitude of the final location
    Lon2: The longitude of the final location
    Locations: The locations between which we are creating a path
    Time: How lng it takes to get from location 1 to location 2 in seconds
    
    Returns
    -------
    The dictionary created from the data
    """
    dictionary = {'lat': [39.259030, 39.256832, 39.255615, 39.254982, 
                          39.254982, 39.256832, 39.254847, 39.255066],
                  'lon': [-76.71479, -76.714385, -76.713958, -76.714275, 
                          -76.714275, -76.714385, -76.713833, -76.714639],
                  'lat2': [39.256832, 39.255615, 39.254982, 39.254847,
                           39.254311, 39.255066, 39.254702, 39.254311],
                  'lon2': [-76.714385, -76.713958, -76.714275, -76.713833,
                           -76.714547, -76.714639, -76.713359, -76.714547],
                  'locations': ['WA(S)->L8-SA', 'L8-SA->UW-FAB_Stair',
                                'UW-FAB_Stair->UW-FAB/ENGR_Stair',
                                'UW-FAB/ENGR_Stair->Stair-FAB/ENGR',
                                'UW-FAB/ENGR_Stair->UW-ENGR/ITE_Stair',
                                'L8-SA->PAHB(E)', 'Stair-FAB/ENGR->CW-FMUE',
                                'PAHB(E)->UW-ENGR/ITE_Stair'],
                  'time': [180, 116, 53, 27, 53, 184, 36, 56]
    }
    df = pd.DataFrame(data=dictionary)
    return df


#############################################################################


#Main for program
st.title("Campus Mapper")
st.subheader("Find the fastest path to class")

#https://deckgl.readthedocs.io/en/latest/layer.html
ALL_LAYERS = {
    "Locations": pdk.Layer(
        "HexagonLayer",
        data=createLatLonDict(),
        get_position=["lon", "lat"],
        radius=10,
        elevation_scale=4,
        elevation_range=[0, 1000],
        extruded=True,
    ),
    "Names": pdk.Layer(
        "TextLayer",
        data=createLatLonDict(),
        get_position=["lon", "lat"],
        get_text="name",
        get_color=[0, 0, 0, 200],
        get_size=12,
        get_alignment_baseline="'bottom'",
    ),
    "Paths": pdk.Layer(
         "ArcLayer",
         data=createPathDict(),
         get_source_position=["lon", "lat"],
         get_target_position=["lon2", "lat2"],
         get_source_color=[200, 30, 0, 160],
         get_target_color=[200, 30, 0, 160],
         auto_highlight=True,
         width_scale=0.0001,
         get_width="outbound",
         width_min_pixels=3,
         width_max_pixels=30,
     )
}

selected_layers = [layer for layer_name, layer in ALL_LAYERS.items()]
if selected_layers:
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={"latitude": 39.255,
                            "longitude": -76.712, "zoom": 14.75, "pitch": 10},
        layers=selected_layers)
    )

st.subheader('Please select your destination')
choice = st.selectbox('Available locations', 
                      ('Lot 8 - Smoking Area',
                       'Upper Walkway - FAB Staircase',
                       'Upper Walkway - FAB/ENGR Staircase',
                       'Staircase - FAB/ENGR', 
                       'Upper Walkway - ENGR/ITE Staircase',
                       'PAHB (E)', 'Center Walkway - FAB/MEYR/UC/ENGR'))

#Pass the chosen destination to path to find a solution
result = path(choice)