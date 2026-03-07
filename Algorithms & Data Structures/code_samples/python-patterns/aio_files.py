import aiohttp
import asyncio
import time
import aiofiles
import json
from pathlib import Path
import os

start_time = time.time()
directory = "test"
if not os.path.exists(directory):
    os.makedirs(directory)


async def get_pokemon(session, url):
    """Get the pokemon files using asynchronous get."""
    end_url = url.split("/")[-1]
    async with session.get(url) as resp:
        pokemon = await resp.json()
        async with aiofiles.open(f"{directory}/poke_{end_url}.json", mode="w") as f:
            await f.write(json.dumps(pokemon))

        return pokemon["name"]


async def get():
    """Create an aiohttp session and pass get_pokemon to event loop"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for number in range(1, 151):
            url = f"https://pokeapi.co/api/v2/pokemon/{number}"
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            print(pokemon)


async def write(filename):
    """Open the json file, parse it, create new text files with subset of data"""
    # Read the contents of the json file.
    async with aiofiles.open(f"{directory}/{filename}", mode="r") as f:
        contents = await f.read()

    # Load it into a dictionary and create a list of moves.
    pokemon = json.loads(contents)
    name = pokemon["name"]
    moves = [move["move"]["name"] for move in pokemon["moves"]]

    # Open a new file to write the list of moves into.
    async with aiofiles.open(f"{directory}/{name}_moves.txt", mode="w") as f:
        await f.write("\n".join(moves))
    return {"name": name, "moves": moves}


async def main():
    """Main function first must await the GET"""
    await get()
    pathlist = Path(directory).glob("*.json")

    # A list to be populated with async tasks.
    tasks = []

    # Iterate through all json files in the directory.
    for path in pathlist:
        tasks.append(asyncio.ensure_future(write(path.name)))

    # Will contain a list of dictionaries containing Pokemons' names and moves
    moves_list = await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
