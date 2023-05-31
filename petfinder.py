import requests
import json

# credentials for the petfinder API
api_key = 'aNCEiHafkArcpvUKdOQS6o9SW2E3ujo0oMoHSP3sYTttQr8l35'
api_secret = 'DYJ4KkyWMcCHMysIEwDTLRwnMIj8Vm1jLoQB1s1f'

def generate_token():
    # generate token
    token = requests.post('https://api.petfinder.com/v2/oauth2/token',
                          data={'grant_type': 'client_credentials',
                                'client_id': api_key,
                                'client_secret': api_secret})
    # convert to json
    token = token.json()

    # save token
    with open('token.json', 'w') as f:
        json.dump(token, f)

    return token

def get_token():
    # get token
    with open('token.json', 'r') as f:
        token = json.load(f)

    if not token:
        token = generate_token()

    return token


def get_pets(pet_type):
    # get token
    # with open('token.json', 'r') as f:
    #     token = json.load(f)
        
    token = get_token()

    # get pets
    pets = requests.get('https://api.petfinder.com/v2/animals',
                        headers={'Authorization': 'Bearer ' + token['access_token']},
                        params={'type': pet_type, 'limit': 100})

    # convert to json
    pets = pets.json()
    pets = pets['animals']

    # save pets
    with open('pets.json', 'w') as f:
        json.dump(pets, f)

    return pets

def get_pet(pet_id):
    # get token
    # with open('token.json', 'r') as f:
    #     token = json.load(f)
        
    token = get_token()

    # get pets
    pet = requests.get(f'https://api.petfinder.com/v2/animals/{pet_id}',
                        headers={'Authorization': 'Bearer ' + token['access_token']},
                        params={'id': pet_id})

    # convert to json
    pet = pet.json()
    pet = pet['animal']

    # save pets
    with open('pet.json', 'w') as f:
        json.dump(pet, f)

    return pet
