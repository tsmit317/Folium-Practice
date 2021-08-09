from re import M
import folium
import folium.features
import folium.plugins
from folium.plugins import fast_marker_cluster
import pandas as pd

usdf = pd.read_csv('usroutes.csv')
kclt = usdf.loc[usdf['source_airport_icao'] == 'KCLT']

map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

folium.TileLayer('openstreetmap').add_to(map)
folium.TileLayer('Stamen Terrain').add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('Stamen Watercolor').add_to(map)
folium.TileLayer('CartoDB dark_matter', attr='Carto').add_to(map)


american_fg = folium.FeatureGroup( name="American Airlines Hubs", show=False)
delta_fg = folium.FeatureGroup( name="Delta Airlines Hubs", show=False)
united_fg = folium.FeatureGroup( name="United Airlines Hubs", show=False)

aa = kclt.loc[kclt['airline'] == 'AA']
delta = kclt.loc[kclt['airline_name'] == 'Delta Air Lines']
united = kclt.loc[kclt['airline_name'] == 'United Airlines']

def create_popup_html(dataframe):
    return """
    <div>
        <p><strong>{name}</strong></p>
        <p style="margin:0;">Airport Code: {ident}</p>
        <p style="margin:0;">Location: {city}, 
        <p style="margin:0;">Elevation: {elevation}ft</p>
        <p style="margin:0;">Location: {city}, {state}</p>
        <a href="{wiki}" target="_blank">Wikipedia</a>  
    </div>
    """.format( name=str(dataframe['dest_airport_name']), 
                ident= str(dataframe['dest_airport_icao']),  
                city=str(dataframe['dest_city']),
                elevation= int(dataframe['dest_altitude']), 
                state= dataframe['dest_state'],
                wiki=dataframe['dest_wiki']
                ), """<div style="white-space: normal">{name} </div>""".format(name=str(dataframe['dest_airport_name']))

def create_line_list(dataframe, fgroup):   
    charll = [35.214001, -80.9431]
    lines = []
    for i in range(len(dataframe)):
        temp = [
                charll,
                [float(dataframe.iloc[i]['dest_lat']), float(dataframe.iloc[i]['dest_lon'])]
        ]
        lines.append(temp)

        popup_html, tool_tip_html = create_popup_html(dataframe.iloc[i])
        lat_lon = [float(dataframe.iloc[i]['dest_lat']), float(dataframe.iloc[i]['dest_lon'])]

        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)

        lg_icon = folium.features.CustomIcon('img/lg_air_icon.png', 
                                                icon_size=(15,15))
        fgroup.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=lg_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
    return lines





american_fg.add_child(folium.PolyLine(create_line_list(aa, american_fg), color='#B61F23', weight=1))
delta_fg.add_child(folium.PolyLine(create_line_list(delta, delta_fg), color='#003268'))
united_fg.add_child(folium.PolyLine(create_line_list(united, united_fg), color='#00fff7'))

map.add_child(american_fg)
map.add_child(delta_fg)
map.add_child(united_fg)
map.add_child(folium.LayerControl())
map.save('usroutemap.html')