import aiohttp

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species"

async def get_pokemon_data(pokemon_name):
    """Fetch Pokemon data from PokeAPI"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{POKEAPI_BASE_URL}/{pokemon_name.lower()}") as response:
            if response.status != 200:
                return None # Pokemon not found
            
            data = await response.json()

            # Fetch generation of pokemon
            async with session.get(f"{SPECIES_URL}/{pokemon_name.lower()}") as species_response:
                species_data = await species_response.json()

            # Parse response for information
            pokemon_info = {
                "name": data["name"].capitalize(),
                "id": data["id"],
                "height": data["height"] / 10,  # Convert dm to meters
                "weight": data["weight"] / 10,  # Convert hg to kg
                "types": [t["type"]["name"].capitalize() for t in data["types"]],
                "abilities": [a["ability"]["name"].replace("-", " ").capitalize() for a in data["abilities"]],
                "moves": [m["move"]["name"].replace("-", " ").capitalize() for m in data["moves"]],
                "generation": species_data["generation"]["name"].replace("generation-", "").upper(),
            }

            return pokemon_info