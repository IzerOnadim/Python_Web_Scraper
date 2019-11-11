import pandas as pd
import requests
from bs4 import BeautifulSoup

# requests the web page at given URL
page = requests.get('https://forecast.weather.gov/MapClick.php?lat=34.05349000000007&lon=-118.24531999999999#.Xcm5i1f7QuU')
# makes scraping webpage easier - finding headings, understandes css etc.
soup = BeautifulSoup(page.content, 'html.parser')
# Everything from the seven day week section from the website.
week = soup.find(id='seven-day-forecast-body')

items = week.find_all(class_='tombstone-container')

periodNames = [item.find(class_='period-name').get_text() for item in items]
shortDesc = [item.find(class_='short-desc').get_text() for item in items]
temps = [item.find(class_='temp').get_text() for item in items]

weatherTable = pd.DataFrame(
    {
        'period': periodNames,
        'short descriptions': shortDesc,
        'temperatures': temps,
    })

print(weatherTable)

weatherTable.to_csv('weather.csv')
