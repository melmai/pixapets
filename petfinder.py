import requests
import json
import os, time

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
    file = 'token.json'
    if not is_token_valid(file):
        token = generate_token()
    else:
        with open(file, 'r') as f:
            token = json.load(f)

    return token

def is_token_valid(token):
    # check if token is valid
    mod_date = os.path.getmtime(token)
    if mod_date + 3600 < time.time():
        return True
    return False


def get_pets(pet_type, **kwargs):        
    token = get_token()
    location = kwargs.get('location', 98404)
    distance = int(kwargs.get('distance', 100))
    breed = kwargs.get('breed', 'all')
    age = kwargs.get('age', 'all')

    request_url = f'https://api.petfinder.com/v2/animals?type={pet_type}&limit=50'
    if location:
        request_url += f'&location={location}&distance={distance}'
    if breed != 'all':
        request_url += f'&breed={breed}'
    if age != 'all':
        request_url += f'&age={age}'

    # get pets
    pets = requests.get(request_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    pets = pets.json()['animals']

    # convert to json
    return pets

def get_pets_by_number(pet_type, number):
    token = get_token()
    
    # get pets
    request_url = f'https://api.petfinder.com/v2/animals?type={pet_type}&limit={number}'
    pets = requests.get(request_url, headers={'Authorization': 'Bearer ' + token['access_token']})

    # convert to json
    return pets.json()['animals']


def get_pet(pet_id):
    token = get_token()

    # get pets
    pet = requests.get(f'https://api.petfinder.com/v2/animals/{pet_id}',
                        headers={'Authorization': 'Bearer ' + token['access_token']})

    # convert to json
    return pet.json()['animal']

def get_breeds(pet_type):
    token = get_token()

    # get pets
    data = requests.get(f'https://api.petfinder.com/v2/types/{pet_type}/breeds',
                            headers={'Authorization': 'Bearer ' + token['access_token']})

    # convert to json
    data = data.json()['breeds']
    # print(data)

    breeds = [("all", "All Breeds")]
    breeds += [(breed['name'], breed['name']) for breed in data]

    return breeds