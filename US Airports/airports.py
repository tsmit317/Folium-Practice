
import folium
import folium.features
import folium.plugins
from folium.plugins import fast_marker_cluster
import pandas as pd
import os
import branca

api_key = os.environ.get('MAPBOX_API_KEY')

df = pd.read_csv('usairports.csv')
md_lg_df = df.loc[(df['type']=='large_airport') | (df['type']=='medium_airport')] # Ignoring small airports for the time being

map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

folium.TileLayer('openstreetmap').add_to(map)
folium.TileLayer('Stamen Terrain').add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('Stamen Watercolor').add_to(map)
folium.TileLayer('CartoDB dark_matter', attr='Carto').add_to(map)

lg = folium.FeatureGroup(name="Large Airports", show=False)
md = folium.FeatureGroup(name="Medium Airports", show=False)


import branca

legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 300px;
    left: 50px;
    width: 280px;
    height: 80px;
    z-index:9999;
    font-size:14px;
    ">
    <p><img src="img/aa-primary.png" alt="Spirit Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;American Airlines Major Hub</p>
    <p><img src="img/delta-icon2.png" alt="Spirit Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Delta Airlines Major Hub</p>
    <p><img src="img/delta-tail.png" alt="Spirit Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Delta Airlines Minor Hub</p>
    <p><img src="img/spirit.png" alt="Spirit Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Spirit Focus City</p>
    <p><img src="img/southwest-prim-blue.png" alt="Southwest Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Southwest Operating Bases</p>
    <p><img src="img/PinClipart.com_southwest-clip-art_3401242.png" alt="Southwest Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Southwest Focus City</p>
    <p><img src="img/united-prim-white.png" alt="United Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;United Airlines Major Hub</p>
    <p><img src="img/alaska-face.png" alt="Alaska Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Alaska Airlines Major Hub</p>
    <p><img src="img/alaska-tail.png" alt="Alaska Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Alaska Airlines Minor Hub</p>

    <p><img src="img/hawaiian2.png" alt="Hawaiian Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Hawaiian Airlines Hub</p>
    <p><img src="img/Frontier-Airlines-Emblem.png" alt="Frontier Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Frontier Airlines Operating Base</p>
    <p><img src="img/frontier-airlines.png" alt="Frontier Logo" width="20" height="20" style="margin-left: 20px"></a>&emsp;Frontier Airlines Focus City</p>

    
    
</div>
<div style="
    position: fixed;
    bottom: 10px;
    left: 50px;
    width: 280px;
    height: 380px;
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    filter: blur(8px);
    -webkit-filter: blur(8px);
    opacity: 0.9;
    ">
</div>
{% endmacro %}
"""

legend = branca.element.MacroElement()
legend._template = branca.element.Template(legend_html)
map.add_child(legend)

def create_popup_html(dataframe):
    return """
    <div>
        <p><strong>{name}</strong></p>
        <p style="margin:0;">Airport Code: {ident}</p>
        <p style="margin:0;">Elevation: {elevation}ft</p>
        <p style="margin:0;">Location: {city}, {state}</p>
        <a href="{wiki}" target="_blank">Wikipedia</a>  
    </div>
    """.format( name=dataframe['name'], 
                ident= dataframe['ident'], 
                elevation= dataframe['elevation_ft'], 
                city=dataframe['municipality'], 
                state= dataframe['iso_region'][-2:],
                wiki=dataframe['wikipedia_link']), """<div style="white-space: normal">{name} </div>""".format(name=dataframe['name'])


for i in range(len(md_lg_df)):
    popup_html, tool_tip_html = create_popup_html(md_lg_df.iloc[i])
        
    lat_lon = [float(md_lg_df.iloc[i]['latitude_deg']), float(md_lg_df.iloc[i]['longitude_deg'])]
    iframe = folium.IFrame(html=popup_html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=200)
    icon = folium.features.CustomIcon('img/lg_air_icon.png' if md_lg_df.iloc[i]['type'] == 'large_airport' else 'img/md_air_icon.png', 
                                     icon_size=(25,25) if md_lg_df.iloc[i]['type'] == 'large_airport' else (15,15))
    
    marker = folium.Marker(location=lat_lon,
                           popup=popup, 
                           icon=icon,
                           tooltip=folium.Tooltip(
                                text=folium.Html(tool_tip_html, script=True, width=150).render()))

    if md_lg_df.iloc[i]['type'] == 'large_airport':
        lg.add_child(marker)
    else:
        md.add_child(marker)


def create_hub_layer(hub_list, fgroup, sub_hub_list= [], primary_icon='img/lg_air_icon.png', secondary_icon='img/secondary.png'):
   
    airline_df = md_lg_df[md_lg_df['ident'].isin(hub_list)]
    main_hub_coord = [float(airline_df.loc[airline_df['ident'] == hub_list[0]]['latitude_deg']), float(airline_df.loc[airline_df['ident'] == hub_list[0]]['longitude_deg'])]
    hub_coord_list = []

    for i in range(len(airline_df)):
        if airline_df.iloc[i]['ident'] != hub_list[0]:
            temp = [
                    main_hub_coord,
                    [float(airline_df.iloc[i]['latitude_deg']), float(airline_df.iloc[i]['longitude_deg'])]
                   ]
            hub_coord_list.append(temp)

        lat_lon = [float(airline_df.iloc[i]['latitude_deg']), float(airline_df.iloc[i]['longitude_deg'])]
       
        popup_html, tool_tip_html = create_popup_html(airline_df.iloc[i])
        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)

        lg_icon = folium.features.CustomIcon(secondary_icon if airline_df.iloc[i]['ident'] in sub_hub_list else primary_icon, 
                                              icon_size=(30,30) if airline_df.iloc[i]['ident'] in sub_hub_list else (35,35))
        fgroup.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=lg_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
    return hub_coord_list



# Create American Airline Hub Layer
american_hubs_fg = folium.FeatureGroup( name="American Airlines Hubs", show=False)
#main hub is first in list
aa_list = ['KDFW','KCLT', 'KPHL', 'KORD', 'KLAX', 'KLGA', 'KMIA', 'KPHX', 'KDCA', 'KJFK']
american_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(aa_list, american_hubs_fg, [], 'img/aa-primary.png', 'img/aa-secondary.png'), color= '#B61F23'))
map.add_child(american_hubs_fg)

# Create Delta Hub Layer    
delta_hubs_fg = folium.FeatureGroup( name="Delta Airlines Hubs", show=False)
delta_list = [ 'KATL', 'KBOS', 'KDTW', 'KLAX', 'KMSP', 'KJFK', 'KLGA', 'KSLC', 'KSEA', 'KAUS', 'KCVG', 'KBNA', 'KRDU', 'KSJC']
delta_list_small = ['KAUS', 'KCVG', 'KBNA', 'KRDU', 'KSJC']
delta_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(delta_list, delta_hubs_fg, delta_list_small, 'img/delta-icon2.png', 'img/delta-tail.png'), color='#003268'))
map.add_child(delta_hubs_fg)

# United Airlines Hub Layer
united_hubs_fg = folium.FeatureGroup( name="United Airlines Hubs", show=False)
united_list = ['KORD', 'KDEN', 'KIAH', 'KLAX', 'KEWR', 'KSFO', 'KIAD']
united_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(united_list, united_hubs_fg, [], 'img/united-prim-white.png', 'img/united-second-yellow.png'), color='#00fff7'))
map.add_child(united_hubs_fg)

# Alaskan Airline Hub Layer
alaskan_hubs_fg = folium.FeatureGroup( name="Alaska Airlines Hubs", show=False)
alaskan_list = ['KSEA', 'PANC', 'KLAX', 'KPDX', 'KSFO', 'KSAN', 'KSJC']
alaskan_list_small = ['KSAN', 'KSJC']
alaskan_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(alaskan_list, alaskan_hubs_fg, alaskan_list_small, 'img/alaska-face.png', 'img/alaska-tail.png'), color='#B3D57D', pulseColor='#00385F'))
map.add_child(alaskan_hubs_fg)

#Hawaiian Airlines Hubs
hawaiian_hubs_fg = folium.FeatureGroup( name="Hawaiian Airlines Hubs", show=False)
hawaiian_list = ['PHNL', 'PHOG', 'PHKO', 'PHLI']
hawaiian_small_list = ['PHKO', 'PHLI']
hawaiian_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(hawaiian_list, 
                                            hawaiian_hubs_fg, hawaiian_small_list,'img/hawaiian2.png', 'img/hawaiian2.png'), color= '#413691'))
map.add_child(hawaiian_hubs_fg)

#Frontier Airlines Hubs
frontier_hubs_fg = folium.FeatureGroup( name="Frontier Airlines Hubs", show=False)
frontier_list = ['KDEN', 'KATL', 'KORD', 'KCLE', 'KCVG', 'KLAS', 'KMCO', 'KPHL', 'KRDU', 'KTTN']
frontier_small_list = frontier_list[1:]
frontier_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(frontier_list, frontier_hubs_fg, frontier_small_list, 'img/Frontier-Airlines-Emblem.png', 'img/Frontier-Airlines.png'), color='#248168'))
map.add_child(frontier_hubs_fg)

#JetBlue Operating
jetblue_hubs_fg = folium.FeatureGroup(name='JetBlue Focus Airports', show=False)
jetblue_list = ['KJFK', 'KBOS', 'KFLL', 'KLGB', 'KMCO', 'KSJU']
jetblue_small_list = jetblue_list[1:]
temp = create_hub_layer(jetblue_list, jetblue_hubs_fg, jetblue_small_list, 'img/jb-prim.png', 'img/jetblue-tail2.png')
map.add_child(jetblue_hubs_fg)

#Southwest Airlines Focus Airports
southwest_hubs_fg = folium.FeatureGroup(name='Southwest Airlines Operating Bases and Focus Cities', show=False)
southwest_list = ['KATL', 'KBWI', 'KMDW', 'KDAL', 'KDEN', 'KHOU', 'KLAS', 'KLAX', 'KOAK', 'KMCO', 'KPHX','KAUS', 'KFLL', 'KBNA', 'KSMF', 'KSAN', 'KSJC', 'KSTL', 'KTPA']
southwest_small_list = ['KAUS', 'KFLL', 'KBNA', 'KSMF', 'KSAN', 'KSJC', 'KSTL', 'KTPA']
temp = create_hub_layer(southwest_list, southwest_hubs_fg, southwest_small_list, 'img/sw-prim.png','img/PinClipart.com_southwest-clip-art_3401242.png' )
map.add_child(southwest_hubs_fg)

#Spirit Airlines
spirit_hubs_fg = folium.FeatureGroup(name='Spirit Arilines Focus Airports', show=False)
spirit_list = ['KACY', 'KORD', 'KDFW', 'KDTW', 'KFLL', 'KLAS', 'KMCO']
spirit_small_list = spirit_list
temp = create_hub_layer(spirit_list, spirit_hubs_fg, spirit_small_list, 'img/spirit.png', 'img/spirit.png')
map.add_child(spirit_hubs_fg)



map.add_child(lg)
map.add_child(md)
map.add_child(folium.LayerControl())

map.save('airportmap.html')