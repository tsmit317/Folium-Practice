import folium
import folium.features
import pandas as pd

data = pd.read_csv('usairports.csv')
map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

lg = folium.FeatureGroup(name="Large Airports")
md = folium.FeatureGroup(name="Medium Airports")



for i in range(1,len(data)):
    if data.iloc[i]['type'] == 'large_airport':
        iframe = folium.IFrame(data.iloc[i]['name'], width=100, height=100)

        popup = folium.Popup(iframe,
                        max_width=100)
        lg_icon = folium.features.CustomIcon('lg_air_icon.png', icon_size=(25,25))
        lg.add_child(folium.Marker(
            location=[float(data.iloc[i]['latitude_deg']), float(data.iloc[i]['longitude_deg'])],
            popup=popup, icon=lg_icon
        ))
        

    elif data.iloc[i]['type'] == 'medium_airport':
        iframe = folium.IFrame(data.iloc[i]['name'], width=100, height=100)

        popup = folium.Popup(iframe,
                        max_width=100)
        md_icon = folium.features.CustomIcon('md_air_icon.png', icon_size=(15,15))
        lg.add_child(folium.Marker(
            location=[float(data.iloc[i]['latitude_deg']), float(data.iloc[i]['longitude_deg'])],
            popup=popup, icon=md_icon
        ))

map.add_child(lg)
map.add_child(md)
map.add_child(folium.LayerControl())
map.save('airportmap.html')