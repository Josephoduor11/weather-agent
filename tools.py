import requests
import os
from dotenv import load_dotenv, find_dotenv
from langchain_core.tools import tool

load_dotenv(find_dotenv())
api_key = os.getenv("WEATHER_API_KEY")


@tool
def weather_tool(city: str) -> str:
    """
    Get the current weather conditions for a specified city.

    Args:
        city: The name of the city to get weather for (e.g., "Nairobi", "London")

    Returns:
        Weather information including temperature and conditions
    """
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']

        return (
            f"Weather in {city}:\n"
            f"• Temperature: {temp}°C (feels like {feels_like}°C)\n"
            f"• Conditions: {description}\n"
            f"• Humidity: {humidity}%"
            f"• Wind Speed: {wind_speed} m/s\n"
            f"• Pressure: {pressure} hPa"
        )

    except Exception as e:
        return f"Error getting weather for {city}: {str(e)}"


@tool
def forecast_tool(city: str) -> str:
    """
    Get the 5-day weather FORECAST for a specified city.
    Use this for future weather predictions (tomorrow, next days).
    """
    try:
        # 5-day forecast endpoint (3-hour intervals)
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Get tomorrow's forecast (first entry after today)
        # The forecast returns 8 entries per day (every 3 hours)
        tomorrow_entries = []
        current_date = None
        tomorrow_forecast = []

        for forecast in data['list']:
            date = forecast['dt_txt'].split()[0]
            if current_date is None:
                current_date = date
                continue
            if date != current_date:
                tomorrow_forecast.append(forecast)
                if len(tomorrow_forecast) >= 4:  # Get 4 entries (12 hours) of tomorrow
                    break

        if not tomorrow_forecast:
            return f"No forecast data available for {city}"

        # Calculate average for tomorrow
        temps = [f['main']['temp'] for f in tomorrow_forecast]
        avg_temp = sum(temps) / len(temps)
        conditions = tomorrow_forecast[0]['weather'][0]['description']

        return f"Forecast for {city} tomorrow: {avg_temp:.1f}°C, {conditions}"

    except Exception as e:
        return f"Error getting forecast for {city}: {str(e)}"
