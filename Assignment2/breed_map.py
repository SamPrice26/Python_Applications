#This code was used to find the corresponding dog names
#on the Dog image API

import requests
import pprint

# Fetch list of available dog breeds from Dog API
def fetch_dog_breeds():    url = "https://dog.ceo/api/breeds/list/all"
    response = requests.get(url)
    data = response.json()
    breeds = data.get("message", {}).keys()
    return breeds

# Generate breed mapping dictionary
def generate_breed_mapping():
    breeds = fetch_dog_breeds()
    breed_mapping = {}
    for breed in breeds:
        # Convert breed name to lowercase and replace spaces with hyphens
        formatted_breed = breed.lower().replace(" ", "-")
        breed_mapping[breed] = formatted_breed
    return breed_mapping

# run and print generate breed
breed_mapping = generate_breed_mapping()
pprint.pprint(breed_mapping)
