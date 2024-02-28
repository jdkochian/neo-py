import requests
from dotenv import load_dotenv
from datetime import date, datetime
import os
from twitter_util import tweet_thread, tweet_at_specific_time
from asteroid_util import plot_asteroid_orbit_from_id, delete_asteroid_plot, get_from_asteroid_id
from emoji import emojize
import schedule 
import time

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
def create_tweets_v1(data): 
    """
    Parse the data returned from `get_nasa_data` and formulate a list of strings corresponding to a thread of tweets per each object.
    """
    res = [] 

    res.append(emojize(f':calendar: Today, {today.strftime("%m/%d/%y")}, there will be {data["element_count"]} NEO\'s making their closest approach.\n\n1/{data["element_count"] + 1} :thread::backhand_index_pointing_down:'))

    for i, entry in enumerate(data['near_earth_objects'][today.strftime('%Y-%m-%d')]): 
        size_data = entry["estimated_diameter"]
        approach_data = entry["close_approach_data"][0]
        time_of_approach = approach_data['close_approach_date_full'].split(' ')[1]
        exact_time_of_approach = datetime.utcfromtimestamp(approach_data['epoch_date_close_approach'] / 1000)
        is_danger = entry["is_potentially_hazardous_asteroid"]

        plot_asteroid_orbit_from_id(entry['id'], entry['name'], exact_time_of_approach)
        # delete_asteroid_plot(entry['id'])
    
        s = ''
        s += emojize(f':comet: {entry["name"]} will be making its close approach at {time_of_approach}.\n :comet:')
        s += emojize(f'Diameter: between {size_data["feet"]["estimated_diameter_min"]:,.0f} and {size_data["feet"]["estimated_diameter_max"]:,.0f} feet across.\n')
        s += emojize(f'At its closest it will be {float(approach_data["miss_distance"]["miles"]):,.0f} miles away, moving at {float(approach_data["relative_velocity"]["miles_per_hour"]):,.0f}mph!\n\n')
        s += emojize(f'{":warning:" if is_danger else ":check_mark_button:"} This asteroid {"is" if entry["is_potentially_hazardous_asteroid"] else "is not"} considered potentially hazardous by NASA {":warning:" if is_danger else ":check_mark_button:"}\n\n')
        s += emojize(f'{i + 2}/{data["element_count"] + 1} :thread:')

        res.append((s, f'tmp/{entry["id"]}.png'))


    return res



def create_tweet_v2(asteroid_data): 
    size_data = asteroid_data['estimated_diameter']
    approach_data = asteroid_data["close_approach_data"][0]
    time_of_approach = approach_data['close_approach_date_full'].split(' ')[1]
    exact_time_of_approach = datetime.utcfromtimestamp(approach_data['epoch_date_close_approach'] / 1000)
    is_danger = asteroid_data["is_potentially_hazardous_asteroid"]


    plot_asteroid_orbit_from_id(asteroid_data['id'], asteroid_data['name'], exact_time_of_approach)


    s = ''
    s += emojize(f':comet: {asteroid_data["name"]} just made its close approach at {time_of_approach}.:comet:\n')
    s += emojize(f'Diameter: between {size_data["feet"]["estimated_diameter_min"]:,.0f} and {size_data["feet"]["estimated_diameter_max"]:,.0f} feet across.\n')
    s += emojize(f'At its closest it will be {float(approach_data["miss_distance"]["miles"]):,.0f} miles away, moving at {float(approach_data["relative_velocity"]["miles_per_hour"]):,.0f}mph!\n\n')
    s += emojize(f'{":warning:" if is_danger else ":check_mark_button:"} This asteroid {"is" if entry["is_potentially_hazardous_asteroid"] else "is not"} considered potentially hazardous by NASA {":warning:" if is_danger else ":check_mark_button:"}\n\n')

    return s


if __name__=="__main__": 
    # This is a proof of concept that I can have code that tweets when the asteroids are nearby 
    # TODO: re-format tweets now that they are not going to be in a thread anymore 
    # TODO: test this system to make sure all objects get reported 
    # TODO: schedule the tewets at the right time, accounting for timezones (this seems to be local)
    data = get_nasa_data()
    for i, entry in enumerate(data['near_earth_objects'][today.strftime('%Y-%m-%d')]): 
        schedule.every().day.at(entry["close_approach_data"][0]['close_approach_date_full'].split(' ')[1]).do(tweet_at_specific_time, tweet=create_tweet_v2(entry), img_src=get_from_asteroid_id(entry['id']))


    while len(schedule.get_jobs()) > 0: 
        schedule.run_pending()
        time.sleep(1)

    # tweets = create_tweets_v1(get_nasa_data())
    # tweet_thread(tweets)
    # pass