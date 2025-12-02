import requests
import datetime as dt
#import json

# openWeather API's base url
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'

# this part loads my API key from a file I inserted the key since it's private
try:
    API_KEY = open('api_key', 'r').read().strip()
except Exception as e:
    print(f'Error: {e}')
    exit() # terminates the program if there's an issue loading the API key

TOWN = 'Techiman'


#function for converting kelvin to celsius and fahrenheit
def kelvin_to_celsius_fahrenheit (kelvin):
     celsius = kelvin - 273.15
     fahrenheit = celsius * (9/5) +32
     return celsius, fahrenheit


#file url
url = BASE_URL + 'appid=' + API_KEY + '&q=' + TOWN

# sending get request to API
print(' ')
try:
    response = requests.get(url, timeout=5).json()
except requests.exceptions.Timeout:
    print('Ooops!! Timed out!') # executes when API takes too long to execute
    exit()
except requests.exceptions.ConnectionError:
    print('...Connection Error! make sure that your device has internet access') #executes when there is an issue with internet connection
    exit()

if response.get('cod')!= 200:
    print(f"API Error{response.get('message','error')}")
    exit()


# extracting data from openWeather
try:
    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)

    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']

    sunrise_time = dt.datetime.fromtimestamp(response['sys']['sunrise'], tz=dt.timezone.utc)
    sunset_time = dt.datetime.fromtimestamp(response['sys']['sunset'], tz=dt.timezone.utc)

except KeyError as e:
    print(f'Oops!! an error occured : {e}')

print(f'-----------------------Weather in {TOWN}--------------------------')
print('')
print(f'Temperature : {temp_celsius:.2f}°C {temp_fahrenheit:.2f}°F')
print(f'Temperature feels like : {feels_like_celsius:.2f}°C {feels_like_fahrenheit:.2f}°F')
print(f'Humidity : {humidity}%')
print(f'wind speed : {wind_speed}m/s')
print(f'General weather : {description}')
print(f'Sunrises at {sunrise_time} UTC')
print(f'Sunset at {sunset_time} UTC')

