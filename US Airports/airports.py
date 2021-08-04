from os import name
import folium
import folium.features
import folium.plugins
from folium.plugins import fast_marker_cluster
import pandas as pd

df = pd.read_csv('usairports.csv')
md_lg_df = df.loc[(df['type']=='large_airport') | (df['type']=='medium_airport')] # Ignoring small airports for the time being

map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

lg = folium.FeatureGroup(name="Large Airports")
md = folium.FeatureGroup(name="Medium Airports")
american_hubs_fg = folium.FeatureGroup(name="American Airlines Hubs", show=False)
delta_hubs_fg = folium.FeatureGroup(name="Delta Airlines Hubs", show=False)
united_hubs_fg = folium.FeatureGroup(name="United Airlines Hubs", show=False)

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




# Create American Airline Hub Layer

aa_list = ['KDFW','KCLT', 'KPHL', 'KORD', 'KLAX', 'KLGA', 'KMIA', 'KPHX', 'KDCA', 'KJFK']
american_df = md_lg_df[md_lg_df['ident'].isin(aa_list)]
kdfw_coord = [float(md_lg_df.loc[md_lg_df['ident'] == 'KDFW']['latitude_deg']), float(md_lg_df.loc[md_lg_df['ident'] == 'KDFW']['longitude_deg'])]
american_hub_coords = []

for i in range(len(american_df)):
    if american_df.iloc[i]['ident'] != 'KDFW':
        temp = [
                kdfw_coord,
                [float(american_df.iloc[i]['latitude_deg']), float(american_df.iloc[i]['longitude_deg'])]
               ]
        american_hub_coords.append(temp)
    
    popup_html, tool_tip_html = create_popup_html(american_df.iloc[i])
    
    lat_lon = [float(american_df.iloc[i]['latitude_deg']), float(american_df.iloc[i]['longitude_deg'])]
    
    iframe = folium.IFrame(html=popup_html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=200)
    lg_icon = folium.features.CustomIcon('img/lg_air_icon.png', icon_size=(25,25))
    american_hubs_fg.add_child(folium.Marker(
        location=lat_lon,
        popup=popup, 
        icon=lg_icon,
        tooltip=folium.Tooltip(
            text=folium.Html(tool_tip_html, script=True, width=150).render(),
        )
    ))


# Create Delta Hub Layer    
delta_list = [ 'KATL', 'KBOS', 'KDTW', 'KLAX', 'KMSP', 'KJFK', 'KLGA', 'KSLC', 'KSEA', 'KAUS', 'KCVG', 'KBNA', 'KRDU', 'KSJC']
delta_list_small = ['KAUS', 'KCVG', 'KBNA', 'KRDU', 'KSJC']

delta_df = md_lg_df[md_lg_df['ident'].isin(delta_list)]
katl_coord = [float(md_lg_df.loc[md_lg_df['ident'] == 'KATL']['latitude_deg']), float(md_lg_df.loc[md_lg_df['ident'] == 'KATL']['longitude_deg'])]
delta_hub_coords = []

for i in range(len(delta_df)):
    if delta_df.iloc[i]['ident'] != 'KATL':
        temp = [
                katl_coord,
                [float(delta_df.iloc[i]['latitude_deg']), float(delta_df.iloc[i]['longitude_deg'])]
               ]
        delta_hub_coords.append(temp)
    
    popup_html, tool_tip_html = create_popup_html(delta_df.iloc[i])
    
    lat_lon = [float(delta_df.iloc[i]['latitude_deg']), float(delta_df.iloc[i]['longitude_deg'])]
    
    iframe = folium.IFrame(html=popup_html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=200)
    lg_icon = folium.features.CustomIcon('img/secondary.png' if delta_df.iloc[i]['ident'] in delta_list_small else 'img/lg_air_icon.png', icon_size=(25,25))
    delta_hubs_fg.add_child(folium.Marker(
        location=lat_lon,
        popup=popup, 
        icon=lg_icon,
        tooltip=folium.Tooltip(
            text=folium.Html(tool_tip_html, script=True, width=150).render(),
        )
    ))


# United Airlines Hub Layer

united_list = ['KORD', 'KDEN', 'KIAH', 'KLAX', 'KEWR', 'KSFO', 'KIAD']
united_df = md_lg_df[md_lg_df['ident'].isin(united_list)]
kord_coord = [float(md_lg_df.loc[md_lg_df['ident'] == 'KORD']['latitude_deg']), float(md_lg_df.loc[md_lg_df['ident'] == 'KORD']['longitude_deg'])]
united_hub_coords = []
for i in range(len(united_df)):
    if united_df.iloc[i]['ident'] != 'KATL':
        temp = [
                kord_coord,
                [float(united_df.iloc[i]['latitude_deg']), float(united_df.iloc[i]['longitude_deg'])]
               ]
        united_hub_coords.append(temp)
    
    popup_html, tool_tip_html = create_popup_html(united_df.iloc[i])
    
    lat_lon = [float(united_df.iloc[i]['latitude_deg']), float(united_df.iloc[i]['longitude_deg'])]
    
    iframe = folium.IFrame(html=popup_html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=200)
    lg_icon = folium.features.CustomIcon('img/lg_air_icon.png', icon_size=(25,25))
    united_hubs_fg.add_child(folium.Marker(
        location=lat_lon,
        popup=popup, 
        icon=lg_icon,
        tooltip=folium.Tooltip(
            text=folium.Html(tool_tip_html, script=True, width=150).render(),
        )
    ))




american_hubs_fg.add_child(folium.plugins.AntPath(american_hub_coords, {"color": "#e60505"}))
map.add_child(american_hubs_fg)

delta_hubs_fg.add_child(folium.plugins.AntPath(delta_hub_coords))
map.add_child(delta_hubs_fg)

united_hubs_fg.add_child(folium.plugins.AntPath(united_hub_coords))
map.add_child(united_hubs_fg)
map.add_child(lg)
map.add_child(md)
map.add_child(folium.LayerControl())
map.save('airportmap.html')