import requests
from dotenv import load_dotenv
from datetime import date
import os
from twitter_util import tweet_thread

today = date.today() 
load_dotenv()

NASA_API_KEY = os.getenv('NASA_API_KEY')

nasa_endpoint = 'https://api.nasa.gov/neo/rest/v1/feed'
params = { 
    'api_key' : NASA_API_KEY, 
    'start_date' : today, 
    'end_date' : today
}

def get_nasa_data(): 
    """
    Hit the nasa NEOWs endpoint for today's date to return the objects that are approaching Earth today.
    """
    try: 
        response = requests.get(nasa_endpoint, params=params)
        if response.status_code == 200: 
            data = response.json()
            return data 
    except: 
        print('Error', response.status_code, response)

#TODO: add emojis
#TODO: format date in first tweet 
def create_tweets(data) -> list[str]: 
    """
    Parse the data returned from `get_nasa_data` and formulate a list of strings corresponding to a thread of tweets per each object.
    """
    res = [] 

    res.append(f'Today, {today}, there will be {data["element_count"]} NEO\'s making their first approach.\n\n1/{data["element_count"] + 1}')
    for i, entry in enumerate(data['near_earth_objects'][today.strftime('%Y-%m-%d')]): 
        size_data = entry["estimated_diameter"]
        approach_data = entry["close_approach_data"][0]
        time_of_approach = approach_data['close_approach_date_full'].split(' ')[1]

        s = ''
        s += f'{entry["name"]} will be making its close approach at {time_of_approach}.\n'
        s += f'Diameter: between {size_data["feet"]["estimated_diameter_min"]:,.0f} and {size_data["feet"]["estimated_diameter_max"]:,.0f} feet across.\n'
        s += f'At its closest it will be {float(approach_data["miss_distance"]["miles"]):,.0f} miles away, moving at {float(approach_data["relative_velocity"]["miles_per_hour"]):,.0f}mph!\n\n'

        s += f'This asteroid {"is" if entry["is_potentially_hazardous_asteroid"] else "is not"} considered potentially hazardous by NASA.\n\n'

        s += f'{i + 2}/{data["element_count"] + 1}'

        res.append(s)

    return res

tweets = create_tweets(get_nasa_data())
tweet_thread(tweets)