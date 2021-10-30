"""
Created on Fri Oct 29 22:38:55 2021

@author: abigailkennedy
"""

import streamlit as st
import pandas as pd
import pydeck as pdk

from urllib.error import URLError

@st.cache
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename)
    return pd.read_json(url)

try:
    ALL_LAYERS = {
        "Data points": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("campus_data.json"),
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Point Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("campus_data.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
    }
    st.sidebar.markdown('### Map Layers')
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": 39.255,
                                "longitude": -76.712, "zoom": 14.75, "pitch": 10},
            layers=selected_layers,
        ))
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error("""
        **This demo requires internet access.**

        Connection error: %s
    """ % e.reason)