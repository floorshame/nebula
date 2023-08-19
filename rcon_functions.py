import valve.rcon
import time 
import shlex
import json
import re

f = open('config.json')
config = json.load(f)

server_address = ("localhost", config["port"])

# -condebug -conclearlog -flushlog -rpt -novid -usercon -ip 0.0.0.0 +rcon_password 123 +net_start

def get_steamids(server_address, password, tf_dir):
    with valve.rcon.RCON(server_address, password) as rcon:
        rcon("status")
    
    owned = []
    
    with open(f'{tf_dir}/console.log', encoding="utf-8") as f:
        lines = f.readlines()
        for line in reversed(lines):
            if ("hostname: Valve Matchmaking Server" in line):
                break
            if ("#" == line[0] and "#TF_" not in line and "userid name" not in line):
                line = shlex.split(line)
                for word in line:
                    if ("[U:1:" in word):
                        owned.append(word)
                    
            

    return owned

steamid64ident = 76561197960265728


def status_steamid(status):
    status_owned = []
    for line in status:
        try:
            for ch in ['[', ']']:
                if ch in line:
                    line = line.replace(ch, '')
            
            usteamid_split = line.split(':')
            commid = int(usteamid_split[2]) + steamid64ident

            status_owned.append(commid)
        except Exception as e:
            return e

    return status_owned

# example command
# print(status_name(get_status(server_address, config["password"], config["dir"])))
