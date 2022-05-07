# DSC 510
# Week 12
# Final Project Openweathermap
# Author Eric Dickey
# 05/30/2021
# The purpose of this program is to call an API to get the weather based on city or zip code

import requests
from requests.exceptions import HTTPError
import json
import re

# API Key for OpenWeather
api_key = "API KEY"
# Openweather URL to build from
base_url = "api.openweathermap.org/data/2.5/weather?q="
# URL for connection test
connection_url = "https://api.openweathermap.org"


# Color class to change text colors easily
class Color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# check to see if we have a connection to the API host
def weather_connection():
    for connect_url in ["https://api.openweathermap.org"]:
        try:
            response = requests.get(connect_url)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print(Color.GREEN + "Success!" + Color.END)
            print("")


# function to handle the zip code lookup
def weather_zip(zip_code):
    zip_url = 'https://api.openweathermap.org/data/2.5/weather?' \
              'q={},us&units=imperial&cnt=24&appid={}'.format(zip_code, api_key)
    weather_response = requests.get(zip_url)
    weather_json = json.loads(weather_response.text)
    # Get the weather data next
    weather_data(weather_json)


# function to handle city state lookup
def weather_city(city, state):
    city_url = 'https://api.openweathermap.org/data/2.5/weather?' \
               'q={},{},us&units=imperial&cnt=24&appid={}'.format(
                city, state, api_key)
    weather_response = requests.get(city_url)
    weather_json = json.loads(weather_response.text)
    # get the weather data next
    weather_data(weather_json)


# function to handle pulling weather data from JSON response
def weather_data(weather_json):
    degree_sign = u"\N{DEGREE SIGN}"
    city_name = weather_json['name']
    current_temp = weather_json['main']['temp']
    temp_min = weather_json['main']['temp_min']
    temp_max = weather_json['main']['temp_max']
    humidity = weather_json['main']['humidity']
    pressure = weather_json['main']['pressure']
    wind_speed = weather_json['wind']['speed']
    cloud_cover = weather_json['clouds']['all']

    print("\n" + "-" * 50)
    print(Color.BOLD + "Here is the weather for " + str(city_name) + Color.END)
    print(Color.GREEN + "- Current Temp: " + Color.END + str(current_temp) + str(degree_sign) + "F")
    print(Color.GREEN + "- Low Temp: " + Color.END + str(temp_min) + str(degree_sign) + "F")
    print(Color.GREEN + "- High Temp: " + Color.END + str(temp_max) + str(degree_sign) + "F")
    print(Color.GREEN + "- Humidity: " + Color.END + str(humidity) + "%")
    print(Color.GREEN + "- Pressure: " + Color.END + str(pressure) + " hPa")
    print(Color.GREEN + "- Wind Speed: " + Color.END + str(wind_speed) + " mph")
    print(Color.GREEN + "- Cloud Coverage: " + Color.END + str(cloud_cover) + "%")
    print("-" * 50 + "\n")


def main():
    print(Color.YELLOW + "-" * 33)
    print(Color.BOLD + "--Welcome to the Weather Center--")
    print("-" * 33 + Color.END)
    print("Checking connection to OpenWeatherMap...")
    weather_connection()

    while True:
        print(Color.UNDERLINE + "Choose one of the following:" + Color.UNDERLINE)
        print(Color.GREEN + "1" + Color.END + " - Lookup weather by zip code")
        print(Color.GREEN + "2" + Color.END + " - Lookup weather by city")
        print(Color.GREEN + "3" + Color.END + " - Quit")
        try:
            menu_choice = input("Please enter your choice: ")
            if menu_choice == '1':
                zip_code = ""
                while zip_code == "":
                    zip_code = input("Enter a 5 digit zip code: ")
                    # valid zip code check
                    is_valid = re.match(r'\b\d{5}$', zip_code)
                    if not is_valid:
                        zip_code = ""
                        print(Color.RED + "\n***Zip code can only be 5 numbers***\n" + Color.END)
                weather_zip(zip_code)
            elif menu_choice == '2':
                city = ""
                while city == "":
                    city = input("Enter a city name: ")
                    # valid city input check
                    is_valid = re.match(r"^[a-zA-Z\-\s]+$", city)
                    if not is_valid:
                        city = ""
                        print(Color.RED + "\n***City has invalid characters***\n" + Color.END)
                state = ""
                while state == "":
                    state = input("Enter a state abbreviation: ")
                    # valid state input check
                    is_valid = re.match(r"[a-zA-Z]{2}$", state)
                    if not is_valid:
                        state = ""
                        print(Color.RED + "\n***State must be 2 letters***\n" + Color.END)
                weather_city(city, state)
            elif menu_choice == '3':
                break
            else:
                print("Error, invalid menu choice.")
        except:
            # zipcode or city had no matches
            print(Color.RED + "\n***No results found***\n" + Color.END)
    print("")
    print("Have a nice day, bye!")


if __name__ == "__main__":
    # execute only if run as a script
    main()
