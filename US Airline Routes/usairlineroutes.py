from os import name
import folium
import folium.features
import folium.plugins
import pandas as pd

# US Routes
usdf = pd.read_csv('usroutes.csv')
krdu = usdf.loc[usdf['source_airport_icao'] == 'KRDU']
kclt = usdf.loc[usdf['source_airport_icao'] == 'KCLT']

# Charlotte Routes 
aa = kclt.loc[kclt['airline'] == 'AA']
delta = kclt.loc[kclt['airline_name'] == 'Delta Air Lines']
united = kclt.loc[kclt['airline_name'] == 'United Airlines']

# Raleigh Routes
aa_krdu = krdu.loc[krdu['airline'] == 'AA']
delta_krdu = krdu.loc[krdu['airline_name'] == 'Delta Air Lines']
ua_krdu = krdu.loc[krdu['airline_name'] == 'United Airlines']

#International Routes
df = pd.read_csv('airroutes.csv')
international = df.loc[(df['source_country'] == 'United States') &  (df['dest_country'] != 'United States')]
international = international.dropna(subset=['dest_lon', 'dest_lat', 'source_lat', 'source_lon'])  
krdu_international = international.loc[international['source_airport_icao'] == 'KRDU']
kclt_international = international.loc[international['source_airport_icao'] == 'KCLT']


map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=4)

folium.TileLayer('openstreetmap').add_to(map)
folium.TileLayer('CartoDB dark_matter', attr='Carto').add_to(map)


def create_popup_html(dataframe, destination_airport):
    if destination_airport:
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
                    elevation= dataframe['dest_altitude'], 
                    state= dataframe['dest_state'],
                    wiki=dataframe['dest_wiki']
                    ), """<div style="white-space: normal">{name} </div>""".format(name=str(dataframe['dest_airport_name']))
    else:
        return """
        <div>
            <p><strong>{name}</strong></p>
            <p style="margin:0;">Airport Code: {ident}</p>
            <p style="margin:0;">Location: {city}, 
            <p style="margin:0;">Elevation: {elevation}ft</p>
            <p style="margin:0;">Location: {city}, {state}</p>
            <a href="{wiki}" target="_blank">Wikipedia</a>  
        </div>
        """.format( name=str(dataframe['source_airport_name']), 
                    ident= str(dataframe['source_airport_icao']),  
                    city=str(dataframe['source_city']),
                    elevation= dataframe['source_altitude'], 
                    state= dataframe['source_state'],
                    wiki=dataframe['source_wiki']
                    ), """<div style="white-space: normal">{name} </div>""".format(name=str(dataframe['source_airport_name']))

def route_tool_tip_html(dataframe):
    return """
    <div>
        <p style="margin:0;"><strong>Airline:</strong> {airline}</p>
        <p style="margin:0;"><strong>From:</strong> {source_name}</p>
        <p style="margin:0;"><strong>To:</strong> {dest_name}</p>
        <p style="margin:0;"><strong>Equipment:</strong> {equip}</p>
        <p style="margin:0;"><strong>Codeshare:</strong> {codeshare}</p>
    </div>
    """.format( airline=str(dataframe['airline']),
                dest_name=str(dataframe['dest_airport_name']),  
                source_name=str(dataframe['source_airport_name']),  
                equip = str(dataframe['equipment']),
                codeshare= 'Yes' if str(dataframe['codeshare']) == 'Y' else 'No' )

def create_source_marker(dataframe, fgroup):
    srcdf = dataframe.drop_duplicates(subset = ["source_airport_icao"])
    for i in range(len(srcdf)):
        popup_html, tool_tip_html = create_popup_html(srcdf.iloc[i], False)
        lat_lon = [float(srcdf.iloc[i]['source_lat']), float(srcdf.iloc[i]['source_lon'])]

        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)

        secondary_icon = folium.features.CustomIcon('img/secondary.png', icon_size=(15,15))

        fgroup.add_child(folium.Marker(
            location=lat_lon,
            popup=popup, 
            icon=secondary_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
    
def create_line_list(dataframe, fgroup, line_color='#9F0000'):   
    for i in range(len(dataframe)):
        temp = [
                [float(dataframe.iloc[i]['source_lat']), float(dataframe.iloc[i]['source_lon'])],
                [float(dataframe.iloc[i]['dest_lat']), float(dataframe.iloc[i]['dest_lon'])]
               ]
        
        # Add PolyLine
        fgroup.add_child(folium.PolyLine(temp, tooltip=route_tool_tip_html(dataframe.iloc[i]), color=line_color))

        popup_html, tool_tip_html = create_popup_html(dataframe.iloc[i], True)
        

        iframe = folium.IFrame(html=popup_html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)

        lg_icon = folium.features.CustomIcon('img/lg_air_icon.png', icon_size=(15,15))

        fgroup.add_child(folium.Marker(
            location=temp[1],
            popup=popup, 
            icon=lg_icon,
            tooltip=folium.Tooltip(
                text=folium.Html(tool_tip_html, script=True, width=150).render(),
            )
        ))
    create_source_marker(dataframe, fgroup)


# Charlotte Routes
american_fg = folium.FeatureGroup( name="KCLT American Airlines", show=False)
create_line_list(aa, american_fg,'#B61F23')
map.add_child(american_fg)

delta_fg = folium.FeatureGroup( name="KCLT Delta Airlines", show=False)
create_line_list(delta, delta_fg, '#003268')
map.add_child(delta_fg)

united_fg = folium.FeatureGroup( name="KCLT United Airlines", show=False)
create_line_list(united, united_fg, '#00fff7')
map.add_child(united_fg)

kclt_international_fg = folium.FeatureGroup(name='KCLT International Routes', show=False)
create_line_list(kclt_international, kclt_international_fg)
map.add_child(kclt_international_fg)

# Ralegh Durham Routes
krdu_delta_fg = folium.FeatureGroup( name='KRDU Delta', show=False)
create_line_list(delta_krdu, krdu_delta_fg, '#003268')
map.add_child(krdu_delta_fg)

krdu_aa_fg = folium.FeatureGroup(name='KRDU American', show=False)
create_line_list(aa_krdu, krdu_aa_fg, '#B61F23')
map.add_child(krdu_aa_fg)

krdu_united_fg = folium.FeatureGroup(name='KRDU United', show=False)
create_line_list(ua_krdu, krdu_united_fg, '#00FFF7')
map.add_child(krdu_united_fg)

krdu_international_fg = folium.FeatureGroup(name='KDRU International Routes', show=False)
create_line_list(krdu_international, krdu_international_fg)
map.add_child(krdu_international_fg)




map.add_child(folium.LayerControl())
map.save('usroutemap.html')