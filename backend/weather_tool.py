import requests
from datetime import datetime, timedelta

def get_weather(
    city: str,
    mode: str = "current",        # current | past | future
    day_offset: int = 0,          # -1 yesterday, +1 tomorrow, +3 future
    condition: str = "summary"    # summary | rain | temperature | wind | humidity
) -> str:

    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)

    if response.status_code != 200:
        return f"Unable to fetch weather data for {city}."

    data = response.json()

    # ================= CURRENT =================
    if mode == "current":
        current = data["current_condition"][0]

        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind = current["windspeedKmph"]

        if condition == "temperature":
            return f"The current temperature in {city} is {temp}°C."
        elif condition == "humidity":
            return f"The humidity in {city} is {humidity}%."
        elif condition == "wind":
            return f"The wind speed in {city} is {wind} km/h."
        elif condition == "rain":
            return f"Currently in {city}, the weather is {desc}."
        else:
            return f"Currently in {city}, it is {temp}°C with {desc}."

    # ================= PAST / FUTURE =================
    index = day_offset

    try:
        day_data = data["weather"][index]
    except IndexError:
        return "Requested date is out of available range."

    avg_temp = day_data["avgtempC"]
    desc = day_data["hourly"][0]["weatherDesc"][0]["value"]
    rain_chance = day_data["hourly"][0]["chanceofrain"]

    date = (
        datetime.now() + timedelta(days=day_offset)
    ).strftime("%Y-%m-%d")

    if condition == "rain":
        return f"On {date} in {city}, the chance of rain was/is {rain_chance}%."
    elif condition == "temperature":
        return f"On {date} in {city}, the average temperature was/is {avg_temp}°C."
    else:
        return f"Weather in {city} on {date}: {avg_temp}°C with {desc}."
