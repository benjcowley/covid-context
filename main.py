import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from keys import tokens
import os
import tweepy

# Twitter Auth
auth = tweepy.OAuthHandler(tokens['api_key'], tokens['api_secret_key'])
auth.set_access_token(tokens['access_key'], tokens['access_secret_key'])
api = tweepy.API(auth)

# Load Data
df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv') 

# Calculation Functions
def slopeIntercept(df):
    df["XY"] = df['new_cases_smoothed_per_million'] * df['new_tests_smoothed_per_thousand']
    df["XX"] = df['new_cases_smoothed_per_million'] * df['new_cases_smoothed_per_million']
    m = ((df['new_cases_smoothed_per_million'].mean()*df['new_tests_smoothed_per_thousand'].mean()) - df["XY"].mean())/((df['new_cases_smoothed_per_million'].mean()**2)-(df["XX"].mean()))
    b = df['new_tests_smoothed_per_thousand'].mean() - (m*df['new_cases_smoothed_per_million'].mean())
    return m, b

def residual(yPred, yObs):
    return yObs - yPred

# Graph 1 & 2 Calculations 
sort = df[df['iso_code'].apply(lambda x: len(x) == 3)]
names = sort['iso_code'].unique()

latestDay = []
for i in names:
    find = sort[sort['iso_code'] == i]
    colTrim = find[['iso_code', 'location', 'new_cases_smoothed_per_million', 'new_tests_smoothed_per_thousand']]
    week = colTrim.tail(7)
    notNull = week[~week.isnull().any(axis=1)].tail(1)
    latestDay.append(notNull)

sortedData = pd.concat(latestDay,ignore_index=True)
sortedData['new_cases_smoothed_per_million'] = sortedData['new_cases_smoothed_per_million'].div(10)
sortedData['new_tests_smoothed_per_thousand'] = sortedData['new_tests_smoothed_per_thousand'].mul(100) # Both to per 100,000

# Graph 1 Chart Prep 
m, b = slopeIntercept(sortedData)
regression = [(m*x)+b for x in sortedData['new_cases_smoothed_per_million']]
sortedData['regression'] = regression
sortedData['residual'] = residual(sortedData["new_tests_smoothed_per_thousand"], sortedData['regression'])
sortedData.sort_values(by=["residual"], inplace = True, ascending=False)
#sortedData.to_csv(r'path.csv', index = False, header = True)

# Graph 2 Chart Prep 
trimmedData = sortedData['iso_code'].head(10)
fortnightData = []
for i in trimmedData:
    data = df.loc[df['iso_code'] == i]
    fortnightData.append(data.tail(14))
plotData = pd.concat(fortnightData,ignore_index=True)
#plotData.to_csv(r'path3.csv', index = False, header = True)
plotData['new_cases_smoothed_per_million'] = plotData['new_cases_smoothed_per_million'].div(10)

# Plot First Graph
fig1 = px.scatter(sortedData, y='new_tests_smoothed_per_thousand', x='new_cases_smoothed_per_million', color="location", labels={
                     "new_tests_smoothed_per_thousand": "Daily New Tests (Smoothed, Per 100k)",
                     "new_cases_smoothed_per_million": "Daily New Cases (Smoothed, Per 100k)",
                 })
fig1.add_trace(go.Scatter(x=sortedData['new_cases_smoothed_per_million'], y=sortedData['regression']))

# Plot Second Graph
fig2 = px.line(plotData, x='date', y='new_cases_smoothed_per_million',color="location",labels={
                     "new_cases_smoothed_per_million": "Daily New Cases (Smoothed, Per 100k)",
                     "date": "Fortnight Trend"})

# Export & Image formmating
getDate = datetime.datetime.now()
date = getDate.strftime("%d%b%y")
if not os.path.exists("images"):
    os.mkdir("images")
fig1.write_image(file=f'images/{date}-Graph1.png')
fig2.write_image(file=f'images/{date}-Graph2.png')

# Twitter Upload
images = (f'images/{date}-Graph1.png', f'images/{date}-Graph2.png')
media_ids = [api.media_upload(i).media_id_string for i in images]
api.update_status(media_ids=media_ids, status="First Picture: Graph displaying the correlation of Testing/Cases by linear regression. \n Second Picture: Covid rates of the last week from the 10 worst performers in Graph 1.")