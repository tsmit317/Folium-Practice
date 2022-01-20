from os import name
import folium
import folium.plugins

map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=6)

amtrak_route = folium.FeatureGroup(name='Amtrak Routes')
amtrak_route.add_child(folium.GeoJson(data=open('Amtrak_Routes.geojson', 'r', encoding='utf-8-sig').read()))


red_style = {'fillColor': '#db0000', 'color': '#000000'} 
station_geo = folium.GeoJson(data=open('Amtrak_Stations.geojson', 'r', encoding='utf-8-sig').read(),
                            marker = folium.CircleMarker(radius = 4, # Radius in metres
                                                         weight = 1, #outline weight
                                                         fill_color = '#000000', 
                                                         fill_opacity = 1),
                            style_function=lambda x: red_style,
                            highlight_function=lambda feature: {"fillcolor": "ff0000", "color": "white"},
                            popup=folium.GeoJsonPopup(fields= ['STNNAME'], aliases= ['Station: ']),
                            tooltip=folium.features.GeoJsonTooltip(fields=['STNNAME'], aliases= ['Station: ']))


amtrak_stations = folium.FeatureGroup(name='Amtrak Stations', show=True)
amtrak_stations.add_child(station_geo)

mini_map = folium.plugins.MiniMap(toggle_display = True)
map.add_child(amtrak_route)
map.add_child(amtrak_stations)
map.add_child(mini_map)
map.add_child(folium.LayerControl())

title_html = '''
             <h3 align="center" style="font-size:16px"><b>Amtrak Routes and Stations</b></h3>
             <h6 align="center" style="font-size:14px"><b>Data Source: 
                <a href="https://data.world/albert/amtrak" target="_blank">
                DataWorld - J. Albert Bowden II </a></b></h6>
             '''
map.get_root().html.add_child(folium.Element(title_html))


map.save('amtrak_routes.html')