import folium
import pandas

"""
Program will read a list of active volcanoes in the United States. It will
plot the longitude, latitude, and elevation and saves it as Map1.html. This also
renders a layer that will show population as well and color map with
green if population is under 10,000,000, orange if the population is between
10,000,000 and 20,000,000, and red if highter that 20,000,000
"""

#import volcanos as data frame object
data = pandas.read_csv("Volcanoes.txt")
#lists of  information in column so we can itterate points on map
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])
#color code points by elevation
def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation <3000:
        return "orange"
    else:
        return "red"


#create map object - base layer
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")

#feature group (list of points to add to map)
fgv=folium.FeatureGroup(name="Volcanoes")
#marker layer
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(el)+ "m",
    fill_color=color_producer(el), color = "grey", fill_opacity=0.7))

fgp=folium.FeatureGroup(name="Population")
#Color code by population - from json file - layer 3
#could add below directly to map but for consistansy should add to feature group
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x:  {'fillColor': 'green' if x['properties']['POP2005']<10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl()) #must be after feature group is added to map
map.save("Map1.html")
