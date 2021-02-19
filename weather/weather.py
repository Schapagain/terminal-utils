import requests
from sys import argv
import os
import datetime
import argparse
import shutil

api_key = os.environ.get("WEATHER_API_KEY") 
days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAYS_IN_A_WEEK = len(days)
units_map = {
    "imperial" : u"\N{DEGREE SIGN}" + 'F',
    "metric" : u"\N{DEGREE SIGN}" + "C",
}

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
    hamilton_lat = "42.8270"
    hamilton_long = "-75.5446"
    units = "metric"
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
    parser = argparse.ArgumentParser(description='Get weather information')
    parser.add_argument(
        'day', 
        nargs = '?',
        choices = [*days,"tomorrow","week","today"], 
        help='day within one week from today',
        )
    parser.add_argument(
        '-u', 
        choices = ['imperial','metric'], 
        help='units to display data in', 
        default = 'metric'
        )
    args = parser.parse_args()

    if args.day is None or args.day == "today":
        day_indices = [0]
    elif args.day == "tomorrow" or args.day == 'morrow':
        day_indices = [(today_idx + 1) % DAYS_IN_A_WEEK]
    elif args.day == "week" or args.day == "this week":
        day_indices = range(0,DAYS_IN_A_WEEK)
    else:
        day_indices = [days.index(args.day)]
        if day_indices[0] <= today_idx:
            day_indices[0] += (DAYS_IN_A_WEEK - today_idx)
    weather_response = get_weather_data(args.u, day_indices)
    if weather_response:
        print_weather(weather_response,units_map[args.u])
    else:
        print("Sorry, I couldn't fetch the weather information right now.")

if __name__ == "__main__" : main()