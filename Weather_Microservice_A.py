import zmq
import requests
import datetime

def get_weather(api_key, location):

    # Open wWather API base URL
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'appid': api_key,
        'units': 'imperial'  # Can use 'metric' for Celsius temps if preferred.
    }

    # Determines if the location is a city/zip code, removes spaces, checks if reamining characters are all valid digits (for zip code)
    if location.replace(" ", "").isdigit():
        # If it's a zip code, adds it to the params with the country code 'US'
        params['zip'] = f"{location},us"
    else:
        # Otherwise, splits the location string by comma and remove the extra spaces.
        parts = [part.strip() for part in location.split(',')]
        # If the location splits into two parts (city and state),
        if len(parts) == 2:
            # If the second part is exactly 2 alphabetic characters (like a state code),
            if len(parts[1]) == 2 and parts[1].isalpha():
                # then format the location as "City,State,US"
                location = f"{parts[0]},{parts[1]},US"
                # Set the query parameter 'q' with the formatted location
            params['q'] = location
        else:
            # If the format is unexpected, just use the location string as is
            params['q'] = location
    # Creates a GET request to the OpenWeatherMap API with the base URL from above and given parameters:
    response = requests.get(base_url, params=params)
     # Checks if the response status code was successful returns JSON response if so.
    if response.status_code == 200:
        return response.json()
    else:
        print("Error when retrieving weather data:", response.status_code, response.text)
        return None

def process_weather_data(data):
    forecasts = data.get("list", [])
    result = {}
    shown_dates = set()
    for forecast in forecasts:
        dt_txt = forecast.get("dt_txt", "")
        date_str = dt_txt.split()[0]
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            #Puts the date in MM-DD-YYYY format for better readability.
            formatted_date = date_obj.strftime("%m-%d-%Y")
        except Exception as e:
            print("Error parsing date:", e)
            formatted_date = date_str
        if formatted_date not in shown_dates:
            weather_info = forecast.get("weather", [{}])
            # Pulls the weather description (like "broken clouds", etc) from the API and capitalizes it
            weather_description = weather_info[0].get("description", "No description").capitalize()
            result[formatted_date] = weather_description
            shown_dates.add(formatted_date)
            if len(shown_dates) == 5:
                break
    return result

def main():

    # INSERT your API key BELOW:
    api_key = "0d12695c2d8fd50f6ea36d4507562bab"  

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    print("Weather microservice running on tcp://*:5555")
    
    while True:
        try:
            message = socket.recv_json()
            print("Received message:", message)
            location = message.get("location", "")
            if not location:
                socket.send_json({"error": "Missing 'location' parameter"})
                continue
            weather_data = get_weather(api_key, location)
            if not weather_data:
                socket.send_json({"error": "Error retrieving weather data"})
                continue
            response = process_weather_data(weather_data)
            socket.send_json(response)
        except Exception as e:
            print("Exception occurred:", str(e))
            socket.send_json({"error": str(e)})

# This makes main() run only if you run this file directly.
# If another file imports it, main() won't run automatically..
# You can delete it if you never import this file.
if __name__ == "__main__":
    main()

