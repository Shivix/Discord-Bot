import sys
import discord
import random
from ISSAPI import ISS

random.seed()

def readServerToken():
    try:
        open("token.txt", "r")
    except OSError:
        print("Could not open token.txt")
        sys.exit(-1)
        
    with open("token.txt", "r") as file:
        lines = file.readlines()
        return lines[1].strip()
    
class client(discord.Client): # (maybe in constructor) ping discord.com?
    ISSdata = ISS()
    clientID = readServerToken()
    messageCount = 0
    prevAuthor = ""
    commandList = "!users\n" \
                  "!tealc\n" \
                  "!eu4wiki\n" \
                  "!run\n" \
                  "!rollthedice\n" \
                  "!whereistheiss"
    botCheck = bool
    
    def getMembers(self):
        return self.get_guild(int(self.clientID)).members
    
    async def on_ready(self):
        print("Bot logged in as {0.user}".format(self)) # confirmation that bot has connected and is ready
        for x in self.get_guild(int(self.clientID)).members:
            if x.bot: # checks if there is another bot on the server to help with commands clashing
                self.botCheck = True
            else:
                self.botCheck = False

    async def on_message(self, message): # is called every time a message is sent by any user
        if message.author == self.user:
            return # stops the bot from replying to itself
        print("Message from {0.author}: {0.content} in channel {0.channel}".format(message))
        
        if message.author == self.prevAuthor:
            self.messageCount += 1
        else:
            self.prevAuthor = message.author
            
        if self.messageCount >= 5:
            await message.channel.send("That's a lot of messages in a row man")
            
        if message.content == "!users":
            await message.channel.send(f"""# of Members {self.get_guild(int(self.clientID)).member_count}""")
            
        elif message.content == "!chatmode":
            await message.delete()
            while True:
                command = input("Type command:")
                if command == "break":
                    break
                else:
                    await message.channel.send(f"""{command}""")
                    
        elif message.content == "!tealc":
            await message.channel.send("Indeed.")
            
        elif message.content == "!eu4wiki":
            await message.channel.send("https://eu4.paradoxwikis.com/Europa_Universalis_4_Wiki")
            
        elif message.content.startswith("!run"):
            if message.content.endswith(".py"):
                await message.channel.send("Indentation error")
            elif message.content.endswith(".cpp"):
                await message.channel.send(f"""Missing semi-colon on line: {random.randint(0, 100)}""")
            elif message.content.endswith(".c"):
                await message.channel.send("Segmentation fault")
            else:
                await message.channel.send("What am I supposed to do with this")
            
        elif message.content == "!help":
            await message.channel.send("Commands:\n" + self.commandList)
            
        elif message.content == "!rollthedice":
            await message.channel.send("The d20 lands on: " + random.randint(1, 20))
            
        elif message.content == "!whereistheiss":
            await message.channel.send(self.ISSdata.position())
        
        elif message.content.startswith("!"): # disabled if another bot is on the server
            await message.channel.send("Error: Unknown command")
            
#    async def on_member_join(self, member):
#        for channel in member.server.channels:
#            if channel == "general":
#                await client.send_message(f"""Welcome to the server {member.mention}, enjoy your stay!""")

