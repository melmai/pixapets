import requests
import json
import os, time

# credentials for the petfinder API
api_key = 'iINAY9o00BynDYDHjGE294wnIP2MiuXXA8tlawH2L0e8jwcNpt'
api_secret = 'yOgc3gLY40k7z1eJKalmMKuzdpir7450mxMLBusX'

def generate_token():
    """Generates a token for the petfinder API"""
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
    """Gets token if not expired, otherwise generates a new one"""
    file = 'token.json'
    
    # check if token exists and is valid
    if os.path.isfile(file) and is_token_valid(file):
        with open(file, 'r') as f:
            token = json.load(f)
    else: # generate new token
        token = generate_token()
        

    return token

def is_token_valid(token):
    """Checks if token is valid"""
    # check if token is valid
    mod_date = os.path.getmtime(token)
    if mod_date + 3600 < time.time():
        return False
    return True


def get_pets(pet_type, **kwargs):
    """Gets pets with optional filters"""       
    # get token
    token = get_token()

    # get arguments
    location = kwargs.get('location', 98404)
    distance = int(kwargs.get('distance', 100))
    breed = kwargs.get('breed', 'all')
    age = kwargs.get('age', 'all')
    number = kwargs.get('number', 50)

    # create request url
    request_url = f'https://api.petfinder.com/v2/animals?type={pet_type}&limit={number}'
    if location:
        request_url += f'&location={location}&distance={distance}'
    if breed != 'all':
        request_url += f'&breed={breed}'
    if age != 'all':
        request_url += f'&age={age}'
    
    # get pets and return as json
    pets = requests.get(request_url, headers={'Authorization': 'Bearer ' + token['access_token']})
    return pets.json()['animals']


def get_pet(pet_id):
    """Gets a single pet by ID"""
    # get pets    
    token = get_token()
    pet = requests.get(f'https://api.petfinder.com/v2/animals/{pet_id}',
                        headers={'Authorization': 'Bearer ' + token['access_token']})

    try: # convert to json
        pet = pet.json()['animal'] 
    except KeyError as e: # if pet not found
        pet = "pet not found"
    
    return pet

def get_breeds(pet_type):
    """Gets breeds by type"""
    # get breeds data
    token = get_token()
    data = requests.get(f'https://api.petfinder.com/v2/types/{pet_type}/breeds',
                            headers={'Authorization': 'Bearer ' + token['access_token']})

    # convert to json
    data = data.json()['breeds']

    # create list of breeds
    breeds = [("all", "All Breeds")]
    breeds += [(breed['name'], breed['name']) for breed in data]

    return breeds