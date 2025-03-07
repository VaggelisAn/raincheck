import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# I need to expand this function, but the weather is just too good:/
def sky_conditions(sky):
    match sky:
        case "ΗΛΙΟΦΑΝΕΙΑ":
            return "sunny"
        case "ΞΑΣΤΕΡΙΑ":
            return "clear"
        case "ΛΙΓΑ ΣΥΝΝΕΦΑ":
            return "few clouds"
        case "ΣΥΝΝΕΦΙΑ":
            return "cloudy"
        case "ΠΟΛΛΑ ΣΥΝΝΕΦΑ":
            return "a lot of clouds"
        case " ΑΣΘΕΝΗ ΒΡΟΧΗ":
            return "light rain"
        case " ΒΡΟΧΗ":
            return "rain"        
        case _:
            return "No prediction."
        
URL = "https://www.forecastweather.gr/προγνωση/ελλαδα/θεσσαλια/βολοσ.html"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')

forecast = []

# Parse html:
rows = soup.select('table tbody tr')
for row in rows:
    time = row.select_one('td').get_text(strip=True)
    time = time[0:2]
    temperature = row.select_one('td:nth-of-type(2) p').get_text(strip=True)
    temperature = int(re.sub('\\D', '', temperature)) # Get temperature as an int
    humidity = row.select_one('td:nth-of-type(3) p').get_text(strip=True)
    humidity = int(re.sub('\\D', '', humidity)) # Get humidity as an int
    sky = row.select_one('td:nth-of-type(5) p').get_text(strip=True)
    sky = sky_conditions(sky)

    forecast.append((time, temperature, humidity, sky))

# Get today's date
today = datetime.now()
# Get the next 5 days in a table
next_5_days = [(today + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(0, 5)]

day = 0
for i in range(len(forecast)):
#   Get next day after time changes
    if (i>0 and forecast[i][0] == "00"):
        day = day+1
    print(f"{next_5_days[day]} at {forecast[i][0]}:00 : {forecast[i][1]}°C, {forecast[i][2]}% hum., {forecast[i][3]}")