
import folium
from numpy import isnan
import pandas as pd

data = pd.read_csv('ski_resort_stats.csv')
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)



for i in range(0,len(data)):
    html ="""
    
    <div>
      <p><strong>{resort}</strong></p>
      
      <p style="margin:0;">Summit: {summit}</p>
      <p style="margin:0;">Base: {base}</p>
      <p style="margin:0;">Vertical: {vert}</p>
      <p style="margin:0;">Number of runs: {runs}</p>
      <p style="margin:0;">Number of lifts: {lifts}</p>
      <div>
        <img style="vertical-align:middle" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Ski_trail_rating_symbol-green_circle.svg/1024px-Ski_trail_rating_symbol-green_circle.svg.png" width="20" height="20">
        <span style="vertical-align:middle">{green}</span>
      </div>
      <div>
        <img style="vertical-align:middle" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Ski_trail_rating_symbol-blue_square.svg/1024px-Ski_trail_rating_symbol-blue_square.svg.png" width="20" height="20">
        <span style="vertical-align:middle">{blue}</span>
      </div>
      <div>
        <img style="vertical-align:middle" src="https://upload.wikimedia.org/wikipedia/commons/0/0c/Ski_trail_rating_symbol-black_diamond.svg" width="20" height="20">
        <span style="vertical-align:middle">{black}</span>
      </div>

    </div>
    """.format(base= "No Info" if pd.isna(data.iloc[i]['base']) else int(data.iloc[i]['base']), 
               summit= "No Info" if pd.isna(data.iloc[i]['summit']) else int(data.iloc[i]['summit']), 
               resort=data.iloc[i]['resort_name'], 
               vert="No Info" if pd.isna(data.iloc[i]['vertical']) else int(data.iloc[i]['vertical']), 
               runs= "No Info" if pd.isna(data.iloc[i]['runs']) else int(data.iloc[i]['runs']),
               lifts="No Info" if pd.isna(data.iloc[i]['lifts']) else int(data.iloc[i]['lifts']),
               green= "{0:.1f}%".format(data.iloc[i]['green_percent'] * 100), 
               blue="{0:.1f}%".format(data.iloc[i]['blue_percent'] * 100),
               black="{0:.1f}%".format(data.iloc[i]['black_percent'] * 100))

    iframe = folium.IFrame(html=html, width=300, height=200)
    desc_html = """<div style="white-space: normal">{name} </div>""".format(name=data.iloc[i]['resort_name'])
    popup = folium.Popup(iframe, max_width=300)
    ski_icon = folium.features.CustomIcon('images/ski-icon2.png', icon_size=(25,25))
    folium.Marker(
      location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
      popup=popup,
      icon=ski_icon,
      tooltip=folium.Tooltip(
        text=folium.Html(desc_html, script=True, width=150).render(),
      )
    ).add_to(m)

title_html = '''
             <h3 align="center" style="font-size:16px"><b>US Ski Resorts</b></h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))
m.save('usskiresorts.html')