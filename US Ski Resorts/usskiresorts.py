import folium
import pandas as pd

data = pd.read_csv('ski_resort_stats.csv')
latitude = 37.0902
longitude = -95.7129
m = folium.Map(location=[latitude, longitude], zoom_start=4)



for i in range(0,len(data)):
    html ="""
    <div>
      <p><strong>{resort}</strong></p>
      <p style="margin:0;">Summit: {summit}</p>
      <p style="margin:0;">Base: {base}</p>
      <p style="margin:0;">Vertical: {vert}</p>
      <p style="margin:0;">Number of runs: {runs}</p>
      <p style="margin:0;">Number of lifts: {lifts}</p>
      <p style="margin:0;">Green Runs: {green}%</p>
      <p style="margin:0;">Blue Runs: {blue}%</p>
      <p style="margin:0;">Black Runs: {black}%</p>

    </div>
    """.format(base=data.iloc[i]['base'], summit= data.iloc[i]['summit'], resort=data.iloc[i]['resort_name'], vert=data.iloc[i]['vertical'],
               runs=data.iloc[i]['runs'], lifts=data.iloc[i]['lifts'], green=data.iloc[i]['green_percent'], blue=data.iloc[i]['blue_percent'],
               black=data.iloc[i]['black_percent'])

    iframe = folium.IFrame(html=html, width=200, height=100)

    popup = folium.Popup(iframe,
                     max_width=200)
    ski_icon = folium.features.CustomIcon('ski-icon2.png', icon_size=(25,25))
    folium.Marker(
      location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
      popup=popup,
      icon=ski_icon
    ).add_to(m)
m.save('usskiresorts.html')