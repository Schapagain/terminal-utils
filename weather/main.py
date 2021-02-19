import requests
from sys import argv
import os
import datetime
from geopy import geocoders
import argparse
import shutil

days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAYS_IN_A_WEEK = len(days)

def print_heading(text,width,subtext=None):

    print(' ' * width)
    text = text.capitalize()
    if subtext:
        text += ' - ' + subtext
    print(text.center(width))
    print(' ' * width)

def print_weather(weather_response,unit):
    for weather in weather_response:
        day, temp_day, feels_like, temp_min, temp_max, desc = weather
        window_width = min(shutil.get_terminal_size((50,20))[0],100)
        day_index = (day + datetime.datetime.today().weekday()) % DAYS_IN_A_WEEK
        print_heading(days[day_index],window_width, desc)
        print(f"Temperature: {temp_day}{unit} ({temp_min}{unit} to {temp_max}{unit})")
        print(f"Feels like: {feels_like}{unit}")
        print(' ' * window_width)

def get_weather_data(units,days):
    api_key = os.environ.get("WEATHER_API_KEY") 
    environ_lat = os.environ.get("WEATHER_LAT")
    environ_long = os.environ.get("WEATHER_LONG")

    hamilton_lat = "42.8270" if not environ_lat else environ_lat
    hamilton_long = "-75.5446" if not environ_long else environ_long
    api_endpoint = f"https://api.openweathermap.org/data/2.5/onecall?lat={hamilton_lat}&lon={hamilton_long}&exclude=hourly,minutely,alerts&appid={api_key}&units={units}"
    
    response = requests.get(api_endpoint)

    if response.status_code != 200:
        return False

    data = []
    response_dict = response.json()
    for day in days:
        response = response_dict['daily'][day]
        temp = response['temp']
        desc = response['weather'][0]['description']
        feels_like = response['feels_like']['day']
        temp_day, temp_min, temp_max = temp['day'], temp['min'], temp['max']
        data.append((day,temp_day,feels_like,temp_min,temp_max,desc))
    return data

def main():
    today_idx = datetime.datetime.today().weekday()
    today = days[today_idx]

    example_usage = '''example:
    weather
    weather today
    weather tomorrow
    weather sunday -u imperial''' 

    parser = argparse.ArgumentParser(
        prog = 'weather',
        epilog = example_usage,
        description='Get weather predictions',
        usage='%(prog)s [day] [options]',
        formatter_class = argparse.RawDescriptionHelpFormatter
        )
    parser.add_argument(
        'day', 
        metavar = 'day',
        nargs = '?',
        type = str.lower,
        choices = [*days,"tomorrow","week","today"], 
        help='name of day within one week from today',
        )
    parser.add_argument(
        '-u',
        '--units',
        metavar='',
        choices = ['imperial','metric'], 
        help='default: (%(default)s) | Allowed units : %(choices)s', 
        default = 'metric'
        )
    args = parser.parse_args()
    if args.day is None or args.day == "today":
        day_indices = [0]
    elif args.day == "tomorrow" or args.day == 'morrow':
        day_indices = [1]
    elif args.day == "week" or args.day == "this week":
        day_indices = range(0,DAYS_IN_A_WEEK)
    else:
        day_indices = [days.index(args.day)]
        if day_indices[0] <= today_idx:
            day_indices[0] += (DAYS_IN_A_WEEK - today_idx)

    units_map = {
        "imperial" : u"\N{DEGREE SIGN}" + 'F',
        "metric" : u"\N{DEGREE SIGN}" + "C",
    }
    try:
        weather_response = get_weather_data(args.units, day_indices)
        if not weather_response: raise Exception()
    except:
        print("Sorry, I couldn't fetch the weather information right now.")
    else:
        print_weather(weather_response,units_map[args.units])
        

if __name__ == "__main__" : main()