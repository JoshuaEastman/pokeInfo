from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon"
SPECIES_URL = "https://pokeapi.co/api/v2/pokemon-species"

# Helper function to map Pokémon names to the API naming convention
def match_api_naming(map_string):
        if map_string.lower() == "zygarde" or map_string.lower() == "zygarde-50" or map_string.lower() == "zygarde-10" or map_string.lower() == "zygarde-100":
            mapped_string = "718"
        elif map_string.lower() == "mr. mime":
            mapped_string = "mr-mime"
        elif map_string.lower() == "mime jr." or map_string.lower() == "mime jr":
            mapped_string = "mime-jr"
        else:
            trans_map = str.maketrans({"♂": "-m", "♀": "-f", "é": "e"})
            mapped_string = map_string.translate(trans_map)
        return mapped_string

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
                "abilities": [],
                "hidden_abilities": [],
                "moves": [m["move"]["name"].replace("-", " ").capitalize() for m in data["moves"]],
                "generation": species_data["generation"]["name"].replace("generation-", "").upper(),
            }

            # Check for hidden abilities
            for ability in data["abilities"]:
                ability_name = ability["ability"]["name"].replace("-", " ").capitalize()
                is_hidden = ability["is_hidden"]
                if is_hidden:
                    pokemon_info["hidden_abilities"].append(ability_name)
                else:
                    pokemon_info["abilities"].append(ability_name)

            return pokemon_info
        
async def merge_sprites(pokemon_id):
    """Merge regular and shiny sprites of a Pokemon"""
    sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
    shiny_sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{pokemon_id}.png"

    async with aiohttp.ClientSession() as session:
        # Fetch regular sprite
        async with session.get(sprite_url) as response:
            regular_sprite = Image.open(io.BytesIO(await response.read()))
        # Fetch shiny sprite
        async with session.get(shiny_sprite_url) as response:
            shiny_sprite = Image.open(io.BytesIO(await response.read()))

    # Resize images to make the consistent in size
    regular_sprite = regular_sprite.resize((200, 200))
    shiny_sprite = shiny_sprite.resize((200, 200))

    # Create new blank image
    combined_width = regular_sprite.width + shiny_sprite.width
    combined_image = Image.new("RGBA", (combined_width, regular_sprite.height))

    # Combine images
    combined_image.paste(regular_sprite, (0, 0))
    combined_image.paste(shiny_sprite, (regular_sprite.width, 0))

    # Save image to buffer as BytesIO object
    img_bytes = io.BytesIO()
    combined_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes