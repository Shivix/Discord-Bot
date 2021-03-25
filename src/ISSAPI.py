import requests

def position():
    posRequest = requests.get("http://api.open-notify.org/iss-now.json")
    
    if posRequest.status_code == 200:  # anything other than 200 can result in unknown data being printed so an exception is set
        posReply = posRequest.json()

        if type(posReply) == dict:
            return "Latitude:", posReply['iss_position']['latitude'] + ", Longitude:", posReply['iss_position'][
                'longitude']
        else:
            return "Error class type:", type(posReply)
    else:
        return "Error:", posRequest.status_code  # prints the exact error code for debugging purposes
