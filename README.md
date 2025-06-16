# pokeInfo

> A modular Discord bot that returns live Pokémon information using the PokéAPI

---

`pokeinfo` is a Python-based Discord bot designed to fetch and display Pokémon data from the [PokéAPI](https://pokeapi.co/). It supports traditional prefix commands and provides details such as stats, types and abilities.

---

## Features

- Command-based Pokémon lookup (e.g. ~pokeinfo pikachu)
- Uses PokéAPI for real-time data
- Embed-rich formatting for stats and abilities
- Modular command structure using discord.ext.commands.Cog
- Voice and TTS capabilities (experimental)

---

## Usage

**Run Locally** *Written with Python 3.10*
```
# Clone and enter repository
git clone https://github.com/RealBeastman/pokeInfo.git
cd pokeInfo

# Setup virtual environment (optional, but recommended)
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create a .env with the following variables
DISCORD_TOKEN=your_discord_token
OPENAI_API_KEY=your_openai_api_key
PERSONAL_USER_ID=your_discord_user_id

# Start the bot
python bot.py
```

**Docker**

`docker compose up --build`

**Example Commands**

`~help`

`~pokeinfo bulbasaur`

`~tts General This is a "spoken" message` *Checks against `personal_user_id` for permission*

---

**Requirements**

- Python 3.10+
- `discord.py`
- `aiohttp`
- `.env` file with specified credentials

---

## Status

**Active:** A side-project I like to dip into occasionally

---

## License

MIT License

---

## Author

Joshua Eastman - contact@joshuaeastman.dev

