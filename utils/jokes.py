import aiohttp

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"

async def get_joke(type=None):
    """Fetch a joke from the JokeAPI"""
    async with aiohttp.ClientSession() as session:
        if type == "single":
            async with session.get(f"{JOKE_API_URL}&type=single") as response:
                if response.status == 200:
                    joke_data = await response.json()
                    return joke_data["joke"]
                else:
                    return "Failed to fetch a joke. Please try again later."
        elif type == "double":
            async with session.get(f"{JOKE_API_URL}&type=twopart") as response: 
                if response.status == 200:
                    joke_data = await response.json()
                    return f"{joke_data['setup']}\n{joke_data['delivery']}"
                else:
                    return "Failed to fetch a joke. Please try again later."
        else:
            async with session.get(f"{JOKE_API_URL}") as response:
                if response.status == 200:
                    joke_data = await response.json()
                    if joke_data["type"] == "single":
                        return joke_data["joke"]
                    elif joke_data["type"] == "twopart":
                        return f"{joke_data['setup']}\n{joke_data['delivery']}"
                else:
                    return "Failed to fetch a joke. Please try again later."