#!/usr/bin/env python3
"""
Weather Forecast Script using National Weather Service API
Fetches daily weather forecast for a given city.
"""

import requests
import sys
from typing import Dict, Any


# City coordinates (latitude, longitude)
CITIES = {
    "Salt Lake City": (40.7608, -111.8910),
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
}

BASE_URL = "https://api.weather.gov"


def get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Fetch weather forecast from NWS API for given coordinates.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location

    Returns:
        Dictionary containing forecast data

    Raises:
        requests.RequestException: If API request fails
    """
    # Set User-Agent header (required by NWS API)
    headers = {
        "User-Agent": "(Weather Forecast Script, contact@example.com)"
    }

    # Step 1: Get grid endpoint from points API
    points_url = f"{BASE_URL}/points/{latitude},{longitude}"

    try:
        points_response = requests.get(points_url, headers=headers, timeout=10)
        points_response.raise_for_status()
        points_data = points_response.json()

        # Step 2: Extract forecast URL
        forecast_url = points_data['properties']['forecast']

        # Step 3: Get forecast data
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        return forecast_data

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        raise
    except KeyError as e:
        print(f"Error parsing API response: {e}")
        raise


def display_forecast(forecast_data: Dict[str, Any]) -> None:
    """
    Display formatted weather forecast.

    Args:
        forecast_data: Dictionary containing forecast information
    """
    properties = forecast_data.get('properties', {})
    periods = properties.get('periods', [])

    if not periods:
        print("No forecast data available.")
        return

    print("\n" + "=" * 70)
    print(f"Weather Forecast for {properties.get('updated', 'Unknown Time')}")
    print("=" * 70 + "\n")

    # Display forecast for each period
    for period in periods:
        name = period.get('name', 'Unknown')
        temperature = period.get('temperature', 'N/A')
        temp_unit = period.get('temperatureUnit', 'F')
        wind_speed = period.get('windSpeed', 'N/A')
        wind_direction = period.get('windDirection', 'N/A')
        short_forecast = period.get('shortForecast', 'No description')
        detailed_forecast = period.get('detailedForecast', 'No details')

        print(f"{name}")
        print(f"  Temperature: {temperature}°{temp_unit}")
        print(f"  Wind: {wind_speed} {wind_direction}")
        print(f"  Conditions: {short_forecast}")
        print(f"  Details: {detailed_forecast}")
        print()


def main():
    """Main function to run the weather forecast script."""
    # Default to Salt Lake City
    city = "Salt Lake City"

    # Check if city name provided as argument
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])

    # Get coordinates for the city
    if city not in CITIES:
        print(f"City '{city}' not found in database.")
        print(f"Available cities: {', '.join(CITIES.keys())}")
        print("\nYou can add coordinates manually by editing the CITIES dictionary.")
        sys.exit(1)

    latitude, longitude = CITIES[city]

    print(f"Fetching weather forecast for {city} ({latitude}, {longitude})...")

    try:
        forecast_data = get_forecast(latitude, longitude)
        display_forecast(forecast_data)
    except Exception as e:
        print(f"Failed to retrieve forecast: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
