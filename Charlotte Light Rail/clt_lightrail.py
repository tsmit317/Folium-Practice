import folium
import folium.plugins


loc = 'Charlotte Public Transportation'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc)   


map = folium.Map(location=[35.245460799023334, -80.8343778182691], zoom_start=12)


blue = folium.FeatureGroup(name='Blue Line')
blue_style = {'fillColor': '#0320fc', 'color': '#0320fc', 'weight': 5} 
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
                style_function=lambda x: red_style))


red_line_route = folium.FeatureGroup(name='Red Line Route')
red_line_route_style = {'fillColor': '#db0000', 'color': '#db0000', 'weight': 5} 
red_line_route.add_child(folium.GeoJson(data=open('data/red_line_route.geojson', 'r', encoding='utf-8-sig').read(),
                style_function=lambda x: red_line_route_style))              


gold = folium.FeatureGroup(name='Gold Line Stops')
gold_style = {'fillColor': '#e3c022', 'color': '#000000'} 
gold.add_child(folium.GeoJson(data=open('data/LYNX_Gold_Line_Stops.geojson', 'r', encoding='utf-8-sig').read(), 
                marker = folium.CircleMarker(radius = 6, # Radius in metres
                                             weight = 1, #outline weight
                                             fill_color = '#000000', 
                                             fill_opacity = 1),
                style_function=lambda x: gold_style))


mini_map = folium.plugins.MiniMap(toggle_display = True)

map.add_child(silver)
map.add_child(blue)
map.add_child(red_line_route)
map.add_child(red_line_stops)
map.add_child(gold)

map.add_child(mini_map)
map.add_child(folium.LayerControl())
map.get_root().html.add_child(folium.Element(title_html))


map.save('lightRail_routes.html')