from os.path import join, exists
from os import makedirs
from fire import Fire
from glob import glob
import json

VERBOSE = False

class Driver(object):
    '''
    The driver is generic and knows how to "pull data" from the dataset. It will pass that 
    to a given engine which formats a data point for the target output using any class that 
    inherits from the base Engine.
    '''

    def __init__(self, engine, root='../../', game_version='v3.0'):
        self.engine = engine
        self.engine.driver = self
        self.game_version = self.engine.game_version
        self.root = root
        self.export = True
        
    def _toggle_writes(self):
        if self.export: self.export = False
        else: self.export = True
        
    def _drive(self, data_path, file_match):
        for src in glob(join(data_path, file_match)):
            if VERBOSE: print(src)
            entry = json.loads(open(src).read())
            yield entry

    def generate_pokedex(self, file_match="*.json"):
        data_path = join(self.root, self.game_version, 'Pokedex')
        records = []
        for entry in self._drive(data_path, file_match):
            record = self.engine.pokedex_entry(entry, self.export)
            records.append(record)
        return records
        
    def generate_moves(self, file_match="*.json"):
        data_path = join(self.root, self.game_version, 'Moves')
        records = []
        for entry in self._drive(data_path, file_match):
            record = self.engine.movedex_entry(entry, self.export)
            records.append(record)
        return records
        
    def generate_abilities(self, file_match="*.json"):
        data_path = join(self.root, self.game_version, 'Abilities')
        records = []
        for entry in self._drive(data_path, file_match):
            record = self.engine.abilitydex_entry(entry, self.export)
            records.append(record)
        return records
        
    def generate_items(self, file_match="*.json"):
        data_path = join(self.root, self.game_version, 'Items')
        records = []
        for entry in self._drive(data_path, file_match):
            record = self.engine.itemdex_entry(entry, self.export)
            records.append(record)
        return records
    
    def generate_natures(self, file_match="*.json"):
        data_path = join(self.root, self.game_version, 'Natures')
        records = []
        for entry in self._drive(data_path, file_match):
            record = self.engine.naturedex_entry(entry, self.export)
            records.append(record)
        return records
    
    def generate_images(self, sets=[]):
        '''For each image set name you provide, call import_images. Setname is a param.'''
        imagesets = ['BookSprites', 'HomeSprites', 'BoxSprites', 'ShuffleTokens', "ItemSprites"]
        if 'ALL' in sets: sets = imagesets
        for s in sets:
            if s in imagesets:
                self.engine.import_images(join(self.root, 'images', s), s)