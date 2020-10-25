from src.client import client

def readBotToken(): # tokens are saved out of source code to keep them private
 
    with open("token.txt", "r") as file: # "r" can be set to "w+" to create the file if it doesnt exist and enable editing in the program
        lines = file.readlines()
        return lines[0].strip()


client = client()
client.run(readBotToken())
