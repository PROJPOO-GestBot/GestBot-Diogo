# GestBot

This is a bot made for communities on Discord with some features like Music, Fun commands and User Level system.

# Directory

*Can be updated in the future*

```
.
├── cogs                # Collection of commands
│   └── Music.py
├── data                # All things that's not code
│   ├── font
│   └── img
├── docs                # Folder with the documentation
├── libs                # Personnal librairies
├── tests               # Folder containing automated tests
├── bot.py              # Bot base file, used to start the bot
├── requirements.txt    # File containing all required dependencies.
├── LICENSE
└── README.md

```
# Prerequisites

Before starting the Bot, you'll need to create a **.env** file, create a Bot on Discord Developer Portal and make a basic discord server to make it work and to use it.

First, let's start with the file needed to be created:
- In the root folder of the discord bot, create a file named **.env** with the informations below (remember to replace where it says **COMPLETE_IT** with the real informations)
``` Env
SQL_HOSTNAME = "localhost"
SQL_PORT = "3306"
SQL_USERNAME = "COMPLETE_IT"
SQL_USER_PASSWORD = "COMPLETE_IT"
SQL_DB_NAME = "GestBot"

BOT_TOKEN = "COMPLETE_IT"

# Take the infos of a Lavalink server on https://lavalink.darrennathanael.com/SSL/lavalink-with-ssl/
LAVALINK_IP = "127.0.0.1"
LAVALINK_PORT = 2333
LAVALINK_PASSWORD = "COMPLETE_IT"
```

After this, let's create a basic Discord Server:
- Open Discord App or use [Discord Web](https://discord.com/app)
- Click on the **+** icon then click on **Create My Own** and after **For me and my friends**. Now give it a name and after click on **Create**.

Let's now create the Bot on Discord Developer Portal and invite it on the Discord Server created before. For this, follow [this tutorial](https://docs.pycord.dev/en/stable/discord.html).

# Installation

If you want to make the bot work, you'll need some things.

- For Linux users
``` bash
sudo apt install python3.10
```

- For Windows users
    - [Download Python 3.10.9 (Latest version of Python 3.10)](https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe)

Now, not all things are installed but these ones are for both OS. Open a **CMD/Terminal** and copy/paste these commands below. This command will automatically install the required dependencies for this project.
```bash
python -m pip install requirements.txt
```

# Testing

Actually, no tests are available, we are searching for a solution to test the code easily.

# Launch the bot

To launch the bot correctly, launch a **CMD/Terminal** in the root folder of the Bot and then, write the command below:
``` bash
python bot.py
```

# Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

# License

[GPLv3](https://github.com/PROJPOO-GestBot/GestBot/blob/main/LICENSE)
