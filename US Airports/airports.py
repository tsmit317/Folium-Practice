import folium
import folium.features
import pandas as pd

df = pd.read_csv('usairports.csv')

md_lg_df = df.loc[(df['type']=='large_airport') | (df['type']=='medium_airport')] # Ignoring small airports for the time being


map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

lg = folium.FeatureGroup(name="Large Airports")
md = folium.FeatureGroup(name="Medium Airports")


for i in range(1,len(md_lg_df)):
    
    
    popup_html ="""
        <div>
            <p><strong>{name}</strong></p>
            <p style="margin:0;">Airport Code: {ident}</p>
            <p style="margin:0;">Elevation: {elevation}ft</p>
            <p style="margin:0;">Location: {city}, {state}</p>
            <a href="{wiki}" target="_blank">Wikipedia</a>  
        </div>
        """.format( name=md_lg_df.iloc[i]['name'], 
                    ident= md_lg_df.iloc[i]['ident'], 
                    elevation= md_lg_df.iloc[i]['elevation_ft'], 
                    city=md_lg_df.iloc[i]['municipality'], 
                    state= md_lg_df.iloc[i]['iso_region'][-2:],
                    wiki=md_lg_df.iloc[i]['wikipedia_link'])
        
    tool_tip_html = """<div style="white-space: normal">{name} </div>""".format(name=md_lg_df.iloc[i]['name'])
    lat_lon = [float(md_lg_df.iloc[i]['latitude_deg']), float(md_lg_df.iloc[i]['longitude_deg'])]

    if md_lg_df.iloc[i]['type'] == 'large_airport':
        
        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)
        lg_icon = folium.features.CustomIcon('img/lg_air_icon.png', icon_size=(25,25))
        lg.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=lg_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
        
    elif md_lg_df.iloc[i]['type'] == 'medium_airport':

        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)
        md_icon = folium.features.CustomIcon('img/md_air_icon.png', icon_size=(15,15))
        md.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=md_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))

map.add_child(lg)
map.add_child(md)
map.add_child(folium.LayerControl())
map.save('airportmap.html')