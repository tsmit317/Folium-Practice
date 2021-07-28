import folium
import pandas as pd

data = pd.read_csv('ski_resort_stats.csv')
latitude = 37.0902
longitude = -95.7129
m = folium.Map(location=[latitude, longitude], zoom_start=4)



for i in range(0,len(data)):
    iframe = folium.IFrame(data.iloc[i]['resort_name'], width=100, height=100)

    popup = folium.Popup(iframe,
                     max_width=100)
    ski_icon = folium.features.CustomIcon('ski-icon2.png', icon_size=(25,25))
    folium.Marker(
      location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
      popup=popup,
      icon=ski_icon
    ).add_to(m)
m.save('usskiresorts.html')