# FunBot

## A Discord nuke bot that is *really* fun for the owner of the server

## Setup

- Copy the `config.env.example` file to `config.env`
- Open up `config.env`
- Change `BOT_TOKEN` to your bot's token
- Add your ID to the `WHITELIST` list *(Multiple IDs are supported)*
- Change `GUILD_ID` to the ID of the server you want to nuke
- Change `AUDIT_MSG` to the message you want to display on every action *(Optional, defaults to "Nuked!")*

## Usage

- Install dependencies: `pip install -r requirements.txt`
- Run the bot: `python3 __main__.py`

The bot will send the audit message you configured to a channel named `#nuked` after it's done.
