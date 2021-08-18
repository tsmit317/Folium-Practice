import folium
import folium.plugins
import pandas as pd


map = folium.Map(location=[35.245460799023334, -80.8343778182691], zoom_start=12)

def create_popup_html(dataframe):
    return """
    <div style="width: 200px;">
        <p style="margin:0;"><b>Station:</b> {name}</p>
        <p style="margin:0;"><b>Platform:</b> {platform}</p>
        <p style="margin:0;"><b>Park and Ride:</b> {par}</p>
        <p style="margin:0;"><b>Parking Spaces:</b> {ps}</p>
        <p style="margin:0;"><b>Bike Locker:</b> {bl}</p>
        <p style="margin:0;"><b>Bike Rack:</b> {br}</p>
          
    </div>
    """.format( name=str(dataframe['NAME']), 
                platform= str(dataframe['Platform']), 
                par=str(dataframe['Park and Ride']), 
                ps= str(dataframe['Parking Spaces']),
                bl=str(dataframe['Bike Locker']),
                br=str(dataframe['Bike Rack'])), """<div style="white-space: normal">{name} </div>""".format(name=dataframe['NAME'])


df = pd.read_csv('data/LYNX_Blue_Line_Stations.csv')
blue_stations_fg = folium.FeatureGroup(name='Blue Line Stations')
blue_style = {'fillColor': '#0320fc', 'color': '#0320fc', 'weight': 5} 
for i in range(len(df)):
    popup_html, tool_tip_html = create_popup_html(df.iloc[i])
    folium.CircleMarker(location=[ float(df.iloc[i]['lat']), float(df.iloc[i]['long'])],
                        popup=popup_html,
                        tooltip=tool_tip_html,
                        radius = 6, # Radius in metres
                        weight = 1, #outline weight
                        fill_color = '##0320fc', 
                        fill_opacity = 1,
                        style_function=lambda x: blue_style,
                        highlight_function=lambda x: {"fillcolor": "ff0000", "color": "white"}).add_to(blue_stations_fg)


blue = folium.FeatureGroup(name='Blue Line')
blue.add_child(folium.GeoJson(data=open('data/LYNX_Blue_Line_Route.geojson', 'r', encoding='utf-8-sig').read(), 
                style_function=lambda x: blue_style))


silver = folium.FeatureGroup(name='Silver Line')
silver_style = {'fillColor': '#4d4d4d', 'color': '#4d4d4d', 'weight': 5} 
silver.add_child(folium.GeoJson(data=open('data/LYNX_Silver_Line_Route.geojson', 'r', encoding='utf-8-sig').read(), 
                style_function=lambda x: silver_style))


red_line_stops = folium.FeatureGroup(name='Red Line Stops')
red_style = {'fillColor': '#db0000', 'color': '#000000'} 
red_line_stops.add_child(folium.GeoJson(data=open('data/LYNX_Red_Line_Station.geojson', 'r', encoding='utf-8-sig').read(),
                marker = folium.CircleMarker(radius = 6, # Radius in metres
                                             weight = 1, #outline weight
                                             fill_color = '#000000', 
                                             fill_opacity = 1),
                style_function=lambda x: red_style,
                highlight_function=lambda feature: {"fillcolor": "ff0000", "color": "white"},
                popup=folium.GeoJsonPopup(fields= ['Name'],
                aliases= ['Station: '])))


red_line_route = folium.FeatureGroup(name='Red Line Route')
red_line_route_style = {'fillColor': '#db0000', 'color': '#db0000', 'weight': 5} 
red_line_route.add_child(folium.GeoJson(data=open('data/red_line_route.geojson', 'r', encoding='utf-8-sig').read(),
                style_function=lambda x: red_line_route_style))              


gold = folium.FeatureGroup(name='Gold Line Stops')
gold_style = {'fillColor': '#e3c022', 'color': '#000000'} 
gold_construction_style = {'fillColor': '#e3c022', 'color': '#fc7703'} 
gold_proposed_style = {'fillColor': '#e3c022', 'color': '#d40007'} 
gold.add_child(folium.GeoJson(data=open('data/LYNX_Gold_Line_Stops.geojson', 'r', encoding='utf-8-sig').read(), 
                marker = folium.CircleMarker(radius = 6, # Radius in metres
                                             weight = 1, #outline weight
                                             fill_color = '#000000', 
                                             fill_opacity = 1),
                style_function=lambda x: gold_style if x['properties']['Status'] == 'Operating' 
                                         else gold_construction_style if x['properties']['Status'] == 'Construction' else gold_proposed_style,
                highlight_function=lambda feature: {"fillcolor": "ffee00", "color": "white"},
                popup=folium.GeoJsonPopup(fields=['Stop_Name', 'Status'],
                aliases= ['Station: ','Status'])))


mini_map = folium.plugins.MiniMap(toggle_display = True)

map.add_child(silver)
map.add_child(blue)
map.add_child(blue_stations_fg)
map.add_child(red_line_route)
map.add_child(red_line_stops)
map.add_child(gold)

map.add_child(mini_map)
map.add_child(folium.LayerControl())

title_html = '''
             <h3 align="center" style="font-size:16px"><b>Charlotte Public Transportation</b></h3>
             <h6 align="center" style="font-size:14px"><b>Data Source: 
                <a href="https://data.charlottenc.gov/search?categories=charlotte%20area%20transit%20system&groupIds=7f5968deb9bc435d851074c93cea6092" target="_blank">
                Charlotte Open Data Portal </a></b></h6>
             '''
map.get_root().html.add_child(folium.Element(title_html))


map.save('lightRail_routes.html')