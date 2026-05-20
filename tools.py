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
