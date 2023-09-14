# nebula (BETA)
A TF2 Cheater databasing tool

# installation

### 1. Python packages needed:
```pip install python-valve tabulate click pymongo sty psutil```

### 2. TF2 startup arguments needed:
```-condebug -conclearlog -flushlog -rpt -novid -usercon -ip 0.0.0.0 +rcon_password 123 +net_start```

### 3. Configure config file

### 4. Download src/release
-> run ```<main.py/.exe> --help``` for commands

### 5. Run a scan
-> run ```<main.py/.exe> scan``` (in a game)

### 5. Report a player
-> run ```<main.py/.exe> report --id <steam_id>```

# How to configure the config file

### Port
-> rcon port (leave as default)

### Password
-> change in the startup commands (or leave as default)

### Dir
-> tf file (change if tf2 isnt on your c drive)

### Steam
-> Steam web api key

### MongoDB
-> Your mongodb cluster (free is fine)
