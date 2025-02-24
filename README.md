**Weather Microservice:

This is a weather microservice that gives you a 5 day forecast. It takes your location (zip code or city, state abbreviation), 
calls the OpenWeatherMap API, and sends back a report with dates (MM-DD-YYYY) and a short weather description
(like "Clear sky" or "Scattered clouds"). It uses ZeroMQ for communication.

NOTE: You have to sign up for OpenWeatherMap (https://openweathermap.org/) and get an API key to use this service.
Here's a short video that explains the API key process for Open Weather Map: https://www.youtube.com/watch?v=MdIfZJ08g2I

**How to request Data:

Create a ZeroMQ request/REQ socket and connect to tcp://localhost:5555.

Send a JSON message with the key "location" and your location in city, comma, state abbreviation or zip code
as the value (Example: { "location": "Portland, OR" }, { "location": "97439" }).

**How to receive Data:

The  icroservice replies with a JSON object, and each key is a date (MM-DD-YYYY), each value is a short weather description.
Example - "02-21-2025": "Few clouds", "02-22-2025": "Scattered clouds"

**UML Diagram:

<img width="949" alt="Weather_Microservice_2" src="https://github.com/user-attachments/assets/c0b66b37-df72-430e-961b-43001c080d4f" />
Weather UML Diagram

**How to run the microservice:

Install dependencies: pip install requests pyzmq
Run the microservice: python weather_microservice.py (python3 weather_microservice.py for macOS)
(The service listens on tcp://localhost:5555)
You may want to sign up for an API key from Open Weather Map, as well. Instructions are on the top of this document.

**Example test client that I used:

import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    #Use a known city format, e.g., "Austin,TX", or zip code "78669"
    request_data = {"location": "Portland, OR"}                     <=== change 'location' value to zip or city,State abbreviation
    socket.send_json(request_data)
    
    response = socket.recv_json()
    print("Response from weather microservice:", response)

if __name__ == "__main__":
    main()









