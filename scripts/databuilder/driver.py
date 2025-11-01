from os.path import join, exists
from os import makedirs
from fire import Fire
from glob import glob
import json

class Driver(object):
    '''
    The driver is generic and knows how to "pull data" from the dataset. It will pass that 
    to a given engine which formats a data point for the target output using any class that 
    inherits from the base Engine.
    '''

    def __init__(self, engine, root=None, game_version=None):
        self.engine = engine
        self.root = root if root else '../../'
        self.game_version = game_version if game_version else self.engine.game_version
        
    def generate_pokedex(self, data_path=None):
        if not data_path: data_path = join(self.root, self.game_version, 'Pokedex')
        for src in glob(data_path+"/*.json"):
            entry = json.loads(open(src).read())
            record = self.engine.pokedex_entry(entry)
        
    def generate_moves(self, data_path=None):
        if not data_path: data_path = join(self.root, self.game_version, 'Moves')
        for src in glob(data_path+"/*.json"):
            entry = json.loads(open(src).read())
            record = self.engine.movedex_entry(entry)
        
    def generate_abilities(self, data_path=None):
        if not data_path: data_path = join(self.root, self.game_version, 'Abilities')
        for src in glob(data_path+"/*.json"):
            entry = json.loads(open(src).read())
            record = self.engine.abilitydex_entry(entry)
        
    def generate_items(self, data_path=None):
        if not data_path: data_path = join(self.root, self.game_version, 'Items')
        for src in glob(data_path+"/*.json"):
            entry = json.loads(open(src).read())
            record = self.engine.itemdex_entry(entry)
    
    def generate_natures(self, data_path=None):
        if not data_path: data_path = join(self.root, self.game_version, 'Natures')
        for src in glob(data_path+"/*.json"):
            entry = json.loads(open(src).read())
            record = self.engine.naturedex_entry(entry)
    
    def generate_images(self, sets=[]):
        '''For each image set name you provide, call import_images. Setname is a param.'''
        imagesets = ['BookSprites', 'HomeSprites', 'BoxSprites', 'ShuffleTokens']
        if 'ALL' in sets: sets = imagesets
        for s in sets:
            if s in imagesets:
                self.engine.import_images(join(self.root, 'images', s), s)