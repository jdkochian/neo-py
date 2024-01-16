import requests
from dotenv import load_dotenv
from datetime import date
import os

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

#TODO: Implement this 
def create_tweets(data) -> list[str]: 
    """
    Parse the data returned from `get_nasa_data` and formulate a list of strings corresponding to a thread of tweets per each object.
    """
    res = [] 

    res.append(f'Today, {today}, there will be {data["element_count"]} NEO\'s making their first approach.\n\n1/{data["element_count"] + 1}')
    for entry in data['near_earth_objects'][today.strftime('%Y-%m-%d')]: 
        res.append(f'{entry["name"]} will be making its close approach at ')

    return res

print(create_tweets(get_nasa_data()))