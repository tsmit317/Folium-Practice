import folium 
import pandas as pd

df = pd.read_csv('owid-covid-data.csv')
covid_df = df.loc[(df['date'] == '2021-08-16') & (df['total_deaths'].notnull()) & (df['location'] != 'World'), ['location', 'total_deaths']] 
covid_df.loc[covid_df['location'] == 'United States', 'location'] = 'United States of America'
covid_df.astype({'location': 'str', 'total_deaths':'float'})


url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'


map = folium.Map(location=[48, -102], zoom_start=3)

# folium.GeoJson(data=open('countries.geojson', 'r', encoding='utf-8-sig').read()),
myscale = (covid_df['total_deaths'].quantile((0,.1,.2,.4,.5,.6,.7,.8,.9,1))).tolist()
folium.Choropleth(
    geo_data=country_shapes,
    name="choropleth",
    data=covid_df,
    columns=['location', 'total_deaths'],
    key_on="feature.properties.name",
    fill_color="YlOrRd",
    threshold_scale=myscale,
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Total Fully Vaccinated",
).add_to(map)

folium.LayerControl().add_to(map)

map.save('covid-world.html')