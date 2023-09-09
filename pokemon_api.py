

import requests
# from requests import get
from IPython.display import Image, display

class Pokemon():
    
    def __init__(self, pokemon):
        self.name = pokemon
        self.weight = None
        self.abilities = [] 
        self.types = []
        self.sprite = None
        self.evolve_chain = []
        self.poke_api_call()
        
    def __repr__(self):
        return (f'\nPokemon: {self.name.capitalize()}')
    
    def poke_api_call(self):
        while True:
            res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{self.name}')
            if res.ok:
                data = res.json()
                self.name = data['name']
                self.weight = data['weight']
                self.abilities = [ability['ability']['name'] for ability in data['abilities']]
                self.types = [poke_type['type']['name'] for poke_type in data['types']]
                self.sprite = self.get_sprite(data)
                self.image = data['sprites']['other']['official-artwork']['front_default']
                break
            else:
                print(f'Invalid Request, status code {res.status_code}. Please enter valid pokemon')
                self.update_pokemon()
        # if not self.evo_chain:
        #   self.find_evo_chain(data['species']['url'])
    
    def evolve_pokemon(self):
            evolve_poke = input(f"\nWhich pokemon does {self.name} evolve into? ").lower()
            res_chain =  requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{evolve_poke}')
            res_chain = requests.get(f'https://pokeapi.co/api/v2/evolution-chain/{self.name}')
            print(f"{self.name.capitalize()} has evolved into {evolve_poke.capitalize()}!\n")
            self.name = evolve_poke
            
            if res_chain.ok:
                data = res_chain.json()
                self.name = data['name']
                self.weight = None
                self.abilities = []
                self.types = []
                self.sprite = None
                self.image = None
                # break
                self.poke_api_call()
            else:
                print(f'Invalid Request, status code {res_chain.status_code}. Please enter valid pokemon')
                # self.update_pokemon()


    # def get_evolve_chain(self, species_url):
    #     res = get(species_url)
    #     if res.ok:
    #         data = res.json()
    #         res = get(data['evolution_chain']['url'])
    #         if res.ok:
    #             data = res.json()
    #             self.populate_evo_chain(data['chain'])
    #             return
    #     print('Try again')
        
    # def populate_evo_chain(self, evo_chain):
    #     self.evo_chain.append(evo_chain['species']['name'])
    #     if evo_chain['evolves_to']:
    #       self.populate_evo_chain(evo_chain['evolves_to'][0])
    #     else:
    #         print(self.evo_chain)
    
    def update_pokemon(self):
        self.name = input('Pokemon name: ')
        
    def get_sprite(self, data):
        animated = data['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
        return animated if animated else data['sprites']['front_default']
    
    def display_img(self):
        display(Image(self.sprite, width=75))
        
    def display_info(self):
        print(f'{self.name} Weight: {self.weight}')
        print('Types: ')
        for poke_type in self.types:
            print(poke_type)
        print('Abilities: ')
        for ability in self.abilities:
            print(ability)
    

my_pokemon = Pokemon('squirtle')

print(my_pokemon)
print(my_pokemon.abilities)
print(my_pokemon.types)
my_pokemon.display_info()

my_pokemon.display_img()

my_pokemon.evolve_pokemon()