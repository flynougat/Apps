import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[40,-99], zoom_start=6, tiles="Stamen Terrain")

fg_volcanoe = folium.FeatureGroup(name="Volcanoe")

for lt, ln, el in zip(lat, lon, elev):
    fg_volcanoe.add_child(folium.CircleMarker(location=[lt, ln], raidus = 1, popup="Elevation"+ str(el)+ "m", fill_color=color_producer(el), 
    fill_opacity = 0.7, color = 'grey'))

fg_population = folium.FeatureGroup(name="population")

fg_population.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x ['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x ['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fg_volcanoe)
map.add_child(fg_population)

map.add_child(folium.LayerControl())

map.save("Map1.html")
