Koneko - A multi purpose Discord bot
------------------------------------
##### Prerequisites   
- Make sure you have docker and docker-compose available on your system
    - [docker](https://www.docker.com/get-started)
    - [docker-compose](https://docs.docker.com/compose/install/)
    
#### Installing
- Download the latest release version of this project.
```bash
git clone https://github.com/mrjamy/KonekoBot.git
```
 - <sub>If you choose not to use git you will need to download the files yourself and would be having a harder time keeping it updated.</sub>
- Set the config files  
 * Global config
 ```bash
 cp config.example.ini config.ini
 nano config.ini
 ```
 Populate the token with your own  
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

#### Run the bot
- Start up docker
- Start the bot itself:
```bash
docker-compose up
```