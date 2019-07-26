# Koneko - A multi purpose Discord bot

### Prerequisites   
- Make sure apt-get is updated
```bash
sudo apt update
```
- #### Python
 * Python 3.6 (or up)
 ```bash
 sudo apt install python3.6
 ```
 * Pip
 ```bash
 sudo apt install python3-pip
 ```
- #### Postgres  
 * Postgres bins
 ```bash
 apt-get install postgresql postgresql-contrib
 ```
 * Configure PostgreSQL to start up upon server boot.
 ```bash
 update-rc.d postgresql enable
 ```
 * Start PostgreSQL.
 ```bash
 service postgresql start
 ```
- #### Git (optional)
```bash
sudo apt-get install git
```
 - <sub>Note - git is used in the guide</sub>

### Installing
- Download the latest release version of this project.
```bash
git clone https://github.com/jmuilwijk/KonekoBot.git
```
 - <sub>If you choose not to use git you will need to download the files yourself and would be having a harder time keeping it updated.</sub>
- Set the config files  
 * Global config
 ```bash
 cp config.example.ini config.ini
 nano config.ini
 ```
 Populate the token and dbl_token with your own  
 Save
 ```bash
 ctrl + x
 y
 ```
 * Database config.
 ```bash
 DIR=$(pwd)
 cd src/util/database
 cp config.example.json config.json
 cd $DIR
 ```

### Run the bot.
```
$ python3 KonekoBot.py
```
