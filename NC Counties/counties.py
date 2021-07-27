import folium
import folium.plugins

map = folium.Map(location=[35.73732766114028, -80.00375707878773], zoom_start=6)

fvg = folium.FeatureGroup(name='Counties')
fvg.add_child(folium.GeoJson(data=open('nccounty.geojson', 'r', encoding='utf-8-sig').read(), 
                            popup=folium.GeoJsonPopup(fields=['County'] )))

mini_map = folium.plugins.MiniMap(toggle_display = True)
map.add_child(fvg)
map.add_child(mini_map)
map.add_child(folium.LayerControl())


map.save('ncmap.html')