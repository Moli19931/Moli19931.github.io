import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.io as pio



df=pd.read_csv('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv')
df=df[['dateRep','cases','deaths','countriesAndTerritories','countryterritoryCode','continentExp']]
#Rename the columns accordingly
df=df.rename(columns={'dateRep' : 'date', 'countriesAndTerritories': 'country', 'countryterritoryCode':'countryCode','continentExp':'continent'})
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
df['date']=df.date.dt.strftime("%Y%m%d")
df=df.sort_values(by=['date'])
df=df.dropna()
print(df[df.cases<0])
df['cases']=df['cases'].abs()

# Now back to your map plotting code...
fig = px.scatter_geo(
    df,
    locations='countryCode',
    color='continent',
    hover_name='country',
    size='cases',
    projection="natural earth",
    title=f'World COVID-19 Cases',
    animation_frame="date"
    )
#fig.show()

pio.write_html(fig, file="InteractiveDashboardCovid19.html", auto_open=True)