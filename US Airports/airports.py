import folium
import folium.features
import pandas as pd

data = pd.read_csv('usairports.csv')
map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

lg = folium.FeatureGroup(name="Large Airports")
md = folium.FeatureGroup(name="Medium Airports")



for i in range(1,len(data)):
    
    
        
    
    if data.iloc[i]['type'] == 'large_airport':
        html ="""
            
            <div>
            <p><strong>{name}</strong></p>
            
            <p style="margin:0;">Airport Code: {ident}</p>
            <p style="margin:0;">Elevation: {elevation}ft</p>
            <p style="margin:0;">Location: {city}, {state}</p>
            
            <a href="{wiki}" target="_blank">Wikipedia</a>
            
            

            </div>
            """.format( name=data.iloc[i]['name'], 
                    ident= data.iloc[i]['ident'], 
                    elevation= data.iloc[i]['elevation_ft'], 
                    city=data.iloc[i]['municipality'], 
                    state= data.iloc[i]['iso_region'][-2],
                    wiki=data.iloc[i]['wikipedia_link'])
        iframe = folium.IFrame(html=html, width=200, height=200)
        tool_tip_html = """<div style="white-space: normal">{name} </div>""".format(name=data.iloc[i]['name'])
        popup = folium.Popup(iframe, max_width=200)
        lg_icon = folium.features.CustomIcon('img/lg_air_icon.png', icon_size=(25,25))
        lg.add_child(folium.Marker(
            location=[float(data.iloc[i]['latitude_deg']), float(data.iloc[i]['longitude_deg'])],
            popup=popup, 
            icon=lg_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )

        ))
        

    elif data.iloc[i]['type'] == 'medium_airport':

        html ="""
    
            <div>
            <p><strong>{name}</strong></p>
            
            <p style="margin:0;">Airport Code: {ident}</p>
            <p style="margin:0;">Elevation: {elevation}ft</p>
            <p style="margin:0;">Location: {city}, {state}</p>
            
            <a href="{wiki}" target="_blank">Wikipedia</a>
            
            

            </div>
            """.format( name=data.iloc[i]['name'], 
                    ident= data.iloc[i]['ident'], 
                    elevation= data.iloc[i]['elevation_ft'], 
                    city=data.iloc[i]['municipality'], 
                    state= data.iloc[i]['iso_region'][-2],
                    wiki=data.iloc[i]['wikipedia_link'])
        iframe = folium.IFrame(data.iloc[i]['name'], width=200, height=200)

        tool_tip_html = """<div style="white-space: normal">{name} </div>""".format(name=data.iloc[i]['name'])
        popup = folium.Popup(iframe, max_width=200)
        md_icon = folium.features.CustomIcon('img/md_air_icon.png', icon_size=(15,15))
        md.add_child(folium.Marker(
            location=[float(data.iloc[i]['latitude_deg']), float(data.iloc[i]['longitude_deg'])],
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