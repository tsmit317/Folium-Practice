from os import name
import folium
import folium.features
import folium.plugins
from folium.plugins import fast_marker_cluster
import pandas as pd

df = pd.read_csv('usairports.csv')
md_lg_df = df.loc[(df['type']=='large_airport') | (df['type']=='medium_airport')] # Ignoring small airports for the time being

map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

lg = folium.FeatureGroup(name="Large Airports", show=False)
md = folium.FeatureGroup(name="Medium Airports", show=False)

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
    
    if md_lg_df.iloc[i]['type'] == 'large_airport':
        lg.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
    else:
        md.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))

def create_hub_layer(hub_list, main_hub, fgroup, sub_hub_list= []):
   
    airline_df = md_lg_df[md_lg_df['ident'].isin(hub_list)]
    main_hub_coord = [float(md_lg_df.loc[md_lg_df['ident'] == main_hub]['latitude_deg']), float(md_lg_df.loc[md_lg_df['ident'] == main_hub]['longitude_deg'])]
    hub_coord_list = []

    for i in range(len(airline_df)):
        if airline_df.iloc[i]['ident'] != main_hub:
            temp = [
                    main_hub_coord,
                    [float(airline_df.iloc[i]['latitude_deg']), float(airline_df.iloc[i]['longitude_deg'])]
                   ]
            hub_coord_list.append(temp)

        popup_html, tool_tip_html = create_popup_html(airline_df.iloc[i])
        lat_lon = [float(airline_df.iloc[i]['latitude_deg']), float(airline_df.iloc[i]['longitude_deg'])]
    
        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)

        lg_icon = folium.features.CustomIcon('img/secondary.png' if airline_df.iloc[i]['ident'] in sub_hub_list else 'img/lg_air_icon.png', 
                                              icon_size=(20,20) if airline_df.iloc[i]['ident'] in sub_hub_list else (25,25))
        fgroup.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=lg_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
    return hub_coord_list

american_hubs_fg = folium.FeatureGroup( name="American Airlines Hubs", show=False)
delta_hubs_fg = folium.FeatureGroup( name="Delta Airlines Hubs", show=False)
united_hubs_fg = folium.FeatureGroup( name="United Airlines Hubs", show=False)
alaskan_hubs_fg = folium.FeatureGroup( name="Alaska Airlines Hubs", show=False)
hawaiian_hubs_fg = folium.FeatureGroup( name="Hawaiian Airlines Hubs", show=False)

# Create American Airline Hub Layer
aa_list = ['KDFW','KCLT', 'KPHL', 'KORD', 'KLAX', 'KLGA', 'KMIA', 'KPHX', 'KDCA', 'KJFK']
american_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(aa_list, 'KDFW', american_hubs_fg), color= '#B61F23'))
map.add_child(american_hubs_fg)


# Create Delta Hub Layer    
delta_list = [ 'KATL', 'KBOS', 'KDTW', 'KLAX', 'KMSP', 'KJFK', 'KLGA', 'KSLC', 'KSEA', 'KAUS', 'KCVG', 'KBNA', 'KRDU', 'KSJC']
delta_list_small = ['KAUS', 'KCVG', 'KBNA', 'KRDU', 'KSJC']
delta_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(delta_list, 'KATL', delta_hubs_fg, delta_list_small), color='#003268'))
map.add_child(delta_hubs_fg)

# United Airlines Hub Layer
united_list = ['KORD', 'KDEN', 'KIAH', 'KLAX', 'KEWR', 'KSFO', 'KIAD']
united_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(united_list, 'KORD', united_hubs_fg), color='#005DAA'))
map.add_child(united_hubs_fg)

# Alaskan Airline Hub Layer
alaskan_list = ['KSEA', 'PANC', 'KLAX', 'KPDX', 'KSFO', 'KSAN', 'KSJC']
alaskan_list_small = ['KSAN', 'KSJC']
alaskan_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(alaskan_list, 'KSEA', alaskan_hubs_fg, alaskan_list_small), color='#B3D57D', pulseColor='#00385F'))
map.add_child(alaskan_hubs_fg)

hawaiian_list = ['PHNL', 'PHOG', 'PHKO', 'PHLI']
hawaiian_small_list = ['PHKO', 'PHLI']
hawaiian_hubs_fg.add_child(folium.plugins.AntPath(create_hub_layer(hawaiian_list, 'PHNL', hawaiian_hubs_fg, hawaiian_small_list), color= '#413691'))
map.add_child(hawaiian_hubs_fg)






map.add_child(lg)
map.add_child(md)
map.add_child(folium.LayerControl())
map.save('airportmap.html')