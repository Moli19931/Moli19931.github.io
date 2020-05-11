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
#print(df[df.cases<0])
df['cases']=df['cases'].abs()

# It may also be interesting to plot cumulative cases over time:
sdf = df.groupby(['countryCode','date']).sum().groupby('countryCode').cumsum().reset_index()
sdf.rename(columns={'cases':'cum_cases'}, inplace=True)
df = df.merge(sdf,on=['countryCode','date']) # Merge cumulative case data back into df
df = df.sort_values(['date','countryCode']) # Re-sort
fig = px.scatter_geo(
df,
locations='countryCode',
color='continent',
hover_name='country',
size="cum_cases",
projection="natural earth",
title=f'World COVID-19 Cumulative Cases',
animation_frame="date"
)

#fig2 = px.bar(df, x="cum_cases", y="country", orientation='h', animation_frame="date")
#fig2.show()

pio.write_html((fig), file="index.html", auto_open=True)