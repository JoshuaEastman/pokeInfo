import aiohttp
import discord

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

async def get_joke():
    async with aiohttp.ClientSession() as session:
        async with session.get(JOKE_API_URL) as response:
            if response.status == 200:
                joke_data = await response.json()
                if joke_data["type"] == "single":
                    return joke_data["joke"]
                else:
                    return f"{joke_data['setup']}\n{joke_data['delivery']}"
            else:
                return "Failed to fetch a joke. Please try again later."