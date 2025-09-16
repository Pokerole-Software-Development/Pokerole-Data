from os.path import join, exists
from os import makedirs
from fire import Fire

class Engine(object):
    
    def __init__(self, output_path, game_version):
        self.output_path = output_path
        self.game_version = game_version
    
    # # These functions take JSON and return a string to be outputted. 
    
    def pokedex_entry(self, entry):
        pass
    def movedex_entry(self, entry):
        pass
    def abilitydex_entry(self, entry):
        pass
    def itemdex_entry(self, entry):
        pass
