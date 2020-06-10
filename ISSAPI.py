import requests


class ISS:

    def __init__(self):
        self.posRequest = requests.get("http://api.open-notify.org/iss-now.json")  # API for positional data of the ISS

    def position(self):
        if self.posRequest.status_code == 200:  # anything other than 200 can result in unknown data being printed so an exception is set
            posReply = self.posRequest.json()

            if type(posReply) == dict:
                return "Latitude:", posReply['iss_position']['latitude'] + ", Longitude:", posReply['iss_position'][
                    'longitude']
            else:
                return "Error class type:", type(posReply)
        else:
            return "Error:", self.posRequest.status_code  # prints the exact error code for debugging purposes
