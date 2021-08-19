import folium 
import pandas as pd

df = pd.read_csv('owid-covid-data.csv')
covid_df = df.loc[(df['date'] == '2021-08-16') & (df['total_deaths'].notnull()) & (df['location'] != 'World'), ['location', 'total_deaths']] 
covid_df.loc[covid_df['location'] == 'United States', 'location'] = 'United States of America'
covid_df.loc[covid_df['location'] == 'Czechia', 'location'] = 'Czech Republic'
covid_df.astype({'location': 'str', 'total_deaths':'float'})


url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'


map = folium.Map(location=[48, -102], zoom_start=3)

# myscale = (covid_df['total_deaths'].quantile((0,.1,.2,.4,.5,.6,.7,.8,.9,1))).tolist()
choro = folium.Choropleth(
    geo_data=country_shapes,
    name="choropleth",
    data=covid_df,
    columns=['location', 'total_deaths'],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Total Deaths",
    highlight=True
)

choro.geojson.add_child(folium.features.GeoJsonTooltip(
        fields=['name'],
        aliases=['Country'],
        style=('background-color: grey; color: white;'),
        localize=True
        ))
map.add_child(choro)
folium.LayerControl().add_to(map)
title_html = '''
             <h3 align="center" style="font-size:16px"><b>COVID-19 Choropleth Map</b></h3>
             <h6 align="center" style="font-size:14px"><b>Data Source: 
                <a href="https://ourworldindata.org/coronavirus" target="_blank"> Our World in Data</a></b></h6>
             '''
map.get_root().html.add_child(folium.Element(title_html))
map.save('covid-world.html')