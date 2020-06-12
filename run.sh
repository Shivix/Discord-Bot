#!/usr/bin/env bash

pip install discord.py #won't do anything if already installed(besides printing that it's installed)

chmod +x bot.py # makes the python file executable

if ! [ -f "tokens.txt" ]; then #ensures the user has added the tokens.txt file
    echo "tokens.txt not found, please refer to README"
    sleep 5
    exit 1
fi

if python bot.py; then # runs the program and returns an exit code
    echo "Success: Exited with code: 0"
else
    echo "ERROR: Exited with code: $?"
fi

sleep 5 # sleeps for a few seconds in case time is needed to read exit code