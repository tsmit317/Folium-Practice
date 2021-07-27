import folium
import folium.plugins

map = folium.Map(location=[40.86736256063699, -94.73893921691446], zoom_start=6)

fvg = folium.FeatureGroup(name='Amtrak Routes')
fvg.add_child(folium.GeoJson(data=open('Amtrak_Routes.geojson', 'r', encoding='utf-8-sig').read()))

mini_map = folium.plugins.MiniMap(toggle_display = True)
map.add_child(fvg)
map.add_child(mini_map)
map.add_child(folium.LayerControl())


map.save('amtrak_routes.html')