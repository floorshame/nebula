# installable packages
import psutil    
from tabulate import tabulate
import click
import pymongo
from pymongo import MongoClient
import sty
from sty import fg
# built in packages
import time
import requests
import os
from os import system
import json
# python files
import rcon_functions as rcon

# vars
nebula_version = "0.1.0.0"

# config
f = open('config.json')
config = json.load(f)

# mongoDB
client = MongoClient(config["mongodb"])

# functions
def steam_request(steamid):
    return requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={config['steam']}&format=json&steamids={steamid}").json()

# click / commands
@click.group()
def cli() -> None:
    f"""
    Nebula {nebula_version}
    """

@cli.command()
@click.option('--id')
def debug(id):
    print(f"{steam_request(id)}")

@cli.command()
def version():
    print(f"{nebula_version}")

@cli.command()
def scan():
    if ("hl2.exe" in (p.name() for p in psutil.process_iter())): # checks if tf2 is open or not
        print("Scanning...")
        status = rcon.get_steamids(("localhost", config["port"]), config["password"], config["dir"])
        time.sleep(2)
        status = rcon.get_steamids(("localhost", config["port"]), config["password"], config["dir"])

        steamIDs = rcon.status_steamid(status)

        if (status == []):
            print("Please join a game first or try again")
        else:
            db = client["nebula"]
            collection = db["cheaters"]

            # player list begins here
            table_data = []
            print("Loading...")
            for i, line in enumerate(steamIDs):
                name = steam_request(int(steamIDs[i]))['response']['players'][0]['personaname'] # this slows down scans but is needed, alternitive would be nice
                doc = collection.find_one({"steam_id": int(steamIDs[i])})
                player_status = f"{fg(255, 0, 0)}ERROR{fg(255, 255, 255)}"

                if (doc == None): # if no reports have been made
                    player_status = f"{fg(0, 255, 0)}legit{fg(255, 255, 255)}"
                else: # if reports have been made
                    player_status = f"{fg(255, 0, 0)}cheater{fg(255, 255, 255)}"

                with open('bot_config.txt') as f: # bot check
                    bot_names = f.readlines()
                    for bot_name in bot_names:
                        if (bot_name.strip().lower() in name.lower()):
                            player_status = f"{fg(255, 0, 0)}bot{fg(255, 255, 255)}"
                    
                table_data.append([f"{fg(255, 255, 255)}{name}", f"{fg(180, 180, 180)}{steamIDs[i]}{fg(255, 255, 255)}", f"{player_status}"])

            # table
            print(f'{fg(255, 255, 255)}{tabulate(table_data, headers=["name", "steamID", "status"], tablefmt="grid")}')

    else: # if tf2 isnt open
        print(f'Please open {fg(207, 106, 50)}Team Fortress 2{fg(255, 255, 255)}')

@cli.command()
@click.option('--id')
def report(id):
    db = client["nebula"]
    collection = db["cheaters"]
    doc = collection.find_one({"steam_id": int(id)})
    if (steam_request(id)['response']['players'] != []): # checks if its a valid steam id
        if (doc == None): #if no reports have been made
            post = { 
                "steam_id": int(id)
            }

            collection.insert_one(post)

            print(f"{steam_request(id)['response']['players'][0]['personaname']} has been added to the database")
        else:
            print(f"{steam_request(id)['response']['players'][0]['personaname']} is already in the database please try and use the 'remove' command")
    else:
        print("Not a valid steam id")

@cli.command()
@click.option('--id')
def search(id):
    db = client["nebula"]
    collection = db["cheaters"]
    doc = collection.find_one({"steam_id": int(id)})
    if (steam_request(id)['response']['players'] != []): # checks if its a valid steam id
        if (doc == None): #if no reports have been made
            print(f"{steam_request(id)['response']['players'][0]['personaname']} -> {fg(0, 255, 0)}legit{fg(255, 255, 255)}")
        else:
            print(f"{steam_request(id)['response']['players'][0]['personaname']} -> {fg(255, 0, 0)}cheater{fg(255, 255, 255)}")
    else:
        print("Not a valid steam id")

@cli.command()
@click.option('--id')
def remove(id):
    db = client["nebula"]
    collection = db["cheaters"]
    doc = collection.find_one({"steam_id": int(id)})
    if (steam_request(id)['response']['players'] != []): # checks if its a valid steam id
        if (doc != None): #if no reports have been made

            collection.delete_one({"steam_id": int(id)})

            print(f"{steam_request(id)['response']['players'][0]['personaname']} has been removed from the database")
        else:
            print(f"{steam_request(id)['response']['players'][0]['personaname']} not found in the database")
    else:
        print("Not a valid steam id")
if __name__ == '__main__':
    cli()