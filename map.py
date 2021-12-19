import folium
import numpy
import pandas

data = pandas.read_excel("Book1.xlsx", sheet_name=0)

lati = list(data["Latitude"])
longi = list(data["Longitude"])
ele = list(data["Elevation"])
name = list(data["Type"])
valid=[]

lati = [x for x in lati if numpy.isnan(x)==False]
longi = [x for x in longi if numpy.isnan(x)==False]
ele = [x for x in ele if numpy.isnan(x)==False]
for x,n in zip(lati, name):
        if numpy.isnan(x)==False:
                valid.append(n)

def color_choice(elevation):
        if elevation<1500:
                return 'green'
        elif 1500<=elevation<3000:
                return 'orange'
        else:
                return 'red'

html = """
Volcano Type:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map = folium.Map(location=[38.2,-99.1], start = 5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, lg, el, nam in zip(lati, longi, ele, valid):
        iframe = folium.IFrame(html=html % (nam, nam, el), width=200, height=100)
        fgv.add_child(folium.Marker(location=[lt, lg], popup=folium.Popup(iframe), icon=folium.Icon(color=color_choice(el))))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json","r", encoding="utf-8-sig").read(), 
style_function= lambda x:{"fillColor":"green" if x["properties"]["POP2005"]<10000000
else "orange" if 10000000 <= x["properties"]["POP2005"]<20000000 else "red"}))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("Map1.html")