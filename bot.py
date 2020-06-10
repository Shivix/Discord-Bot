from client import client

def readBotToken(): # tokens are saved out of source code to keep them private
    with open("token.txt", "r") as file:
        lines = file.readlines()
        return lines[0].strip()


client = client()
client.run(readBotToken())
