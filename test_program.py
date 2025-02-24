import zmq


def main():

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")


    #Use a known city format, such as, "Austin,TX", or zip code "78669"
    request_data = {"location": "97439"}
    socket.send_json(request_data)
    


    response = socket.recv_json()
    print("Response from weather microservice:", response)


if __name__ == "__main__":
    main()
