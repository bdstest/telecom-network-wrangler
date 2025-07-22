#!/usr/bin/env python3
"""
Create GIS Network Coverage Visualization
Author: bdstest
"""

import folium
import json

# Create a map centered on NYC
m = folium.Map(location=[40.7428, -73.9875], zoom_start=12)

# Network site data
sites = [
    {"coords": [40.7128, -74.0059], "id": "NYC001", "gen": "5G", "signal": -75, "coverage_km": 2.1, "color": "red"},
    {"coords": [40.7484, -73.9857], "id": "NYC002", "gen": "4G/5G", "signal": -82, "coverage_km": 3.8, "color": "blue"},
    {"coords": [40.7831, -73.9712], "id": "NYC003", "gen": "5G", "signal": -70, "coverage_km": 2.5, "color": "red"},
    {"coords": [40.7589, -73.9851], "id": "NYC004", "gen": "4G", "signal": -85, "coverage_km": 4.2, "color": "green"}
]

# Add sites to map
for site in sites:
    # Add coverage circle
    folium.Circle(
        location=site["coords"],
        radius=site["coverage_km"] * 1000,  # km to meters
        color=site["color"],
        fill=True,
        fillOpacity=0.1,
        popup=f"{site['id']} - {site['gen']}<br>Signal: {site['signal']} dBm<br>Coverage: {site['coverage_km']} km"
    ).add_to(m)
    
    # Add site marker
    folium.Marker(
        location=site["coords"],
        popup=f"<b>{site['id']}</b><br>{site['gen']} Network<br>Signal: {site['signal']} dBm",
        icon=folium.Icon(color=site["color"], icon="signal")
    ).add_to(m)

# Add title
title_html = '''
<h3 align="center" style="font-size:20px"><b>Telecom Network Wrangler - NYC 5G/4G Coverage Map</b></h3>
<p align="center">Geographic Information System (GIS) Visualization by bdstest</p>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save map
m.save('telecom_gis_coverage_map.html')
print("Map saved as 'telecom_gis_coverage_map.html'")
print("Open this file in a browser to view the interactive map")