import sys
import discord
import random
from src.ISSAPI import position

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

async def run_file(message):
    if message.content.endswith(".py"):
        await message.channel.send("Indentation error")
    elif message.content.endswith(".cpp"):
        await message.channel.send(f"""Missing semi-colon on line: {random.randint(0, 100)}""")
    elif message.content.endswith(".c"):
        await message.channel.send("Segmentation fault")
    else:
        await message.channel.send("What am I supposed to do with this")

async def dice_roll(message):
    await message.channel.send(f"""The d20 lands on: " + {random.randint(1, 20)}""")

async def iss_pos(message):
    await message.channel.send(position())

class client(discord.Client):
    def __init__(self, **options):
        
        # get commands from file
        with open("textCommands.txt", 'r') as file:
            for line in file:
                (key, command) = line.strip().split('|')
                self.text_commands.update({key: command})
                
        # create command list string for printing help command
        super().__init__(**options)
        for key in self.text_commands.keys():
            self.command_list += '\n'
            self.command_list += key
        for key in self.adv_commands.keys():
            self.command_list += '\n'
            self.command_list += key

    async def user_count(self, message):
        await message.channel.send(f"""# of Members {self.get_guild(int(self.client_ID)).member_count}""")
    
    async def help(self, message):
        await message.channel.send(self.command_list)
        
    client_ID = readServerToken()
    command_prefix = '!'
    message_count = 0
    prev_author = ""
    text_commands = {"!tealc": "Indeed."}

    adv_commands = {"!users": user_count,
                    "!run": run_file,
                    "!rollthedice": dice_roll,
                    "!whereistheiss": iss_pos,
                    "!help": help}
    
    command_list = "Commands:"
    has_other_bot = bool

    def getMembers(self):
        return self.get_guild(int(self.client_ID)).members

    async def on_ready(self):
        print("Bot logged in as {0.user}".format(self))  # confirmation that bot has connected and is ready
        for x in self.get_guild(int(self.client_ID)).members:
            if x.bot:  # checks if there is another bot on the server to help with commands clashing
                self.has_other_bot = True
                print("Another bot has been detected on the server.")
            else:
                self.has_other_bot = False

    async def get_command(self, message):
        if message.content in self.text_commands:
            await message.channel.send(self.text_commands[message.content])
        elif message.content in self.adv_commands:
            self.adv_commands[message.content](message)
        elif message.content.startswith(self.command_prefix):
            if not self.has_other_bot:
                await message.channel.send("Command not found")

    async def on_message(self, message):  # is called every time a message is sent by any user
        if message.author == self.user:
            return  # stops the bot from replying to itself
        print("Message from {0.author}: {0.content} in channel {0.channel}".format(message))

        if message.author == self.prev_author:
            self.message_count += 1
        else:
            self.prev_author = message.author

        if self.message_count >= 5:
            await message.channel.send("That's a lot of messages in a row man")

#    async def on_member_join(self, member):
#        for channel in member.server.channels:
#            if channel == "general":
#                await client.send_message(f"""Welcome to the server {member.mention}, enjoy your stay!""")
