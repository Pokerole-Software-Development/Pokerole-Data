import yaml
from glob import glob
import json
import os
import pandas as pd
import re
from shutil import copy
import fire
import time
import datetime

secrets = json.load(open('../../secrets.json'))

class Foundry(object):
    
    def __init__(self, version="Version20", public_vault=False):
        self.obsidian = secrets['PublicObsidianRoot'] if public_vault else secrets['ObsidianRoot']
        self.path_setup(version)
        self.version = version

    def path_setup(self, version):
        
        self.pokedex_path = f'../../{version}/Pokedex'
        self.abilities_path = f'../../{version}/Abilities'
        self.moves_path = f'../../{version}/Moves'
        self.learnsets_path = f'../../{version}/Learnsets'
        self.natures_path = f'../../{version}/Natures'
        self.sprites_path = '../../Images/BoxSprites/'
        self.home_path = '../../Images/HomeSprites/'
        self.book_path = '../../Images/BookSprites/'
        self.shuffle_path = '../../Images/ShuffleTokens/'
        self.items_path = f'../../{version}/Items/'

        paths = [self.pokedex_path,self.abilities_path,self.moves_path,
        self.learnsets_path,self.natures_path,self.sprites_path,
        self.home_path,self.book_path,self.shuffle_path,self.items_path]
        
        for p in paths:
            if not os.path.exists(p): raise Exception(f"ERROR: Path {p} not found!")
            
        self.pokedex_output = '../../Foundry/'
        self.abilities_output = '../../Foundry/'
        self.moves_output = '../../Foundry/'
        self.learnsets_output = '../../Foundry/'
        self.natures_output = '../../Foundry/'
        self.sprites_output = '../../Foundry/'
        self.home_output = '../../Foundry/'
        self.book_output = '../../Foundry/'
        self.shuffle_output = '../../Foundry/'
        self.items_output = '../../Foundry/'

        self.outputs = [self.pokedex_output,self.abilities_output,self.moves_output,
                    self.learnsets_output,self.natures_output,self.sprites_output,
                    self.home_output,self.book_output,self.shuffle_output,self.items_output]

        for p in self.outputs:
            os.makedirs(p,exist_ok=True)
            
        return 0

    def _pokedex(self):
        pass
    
    def _abilities(self):
        pass
    
    def _moves(self):
        
        def _attribute_get(attr, value):
            if not attr: return False
            else: return attr.get(value) if attr.get(value) else False
        
        db = []
        for src in glob(self.moves_path+"/*.json"):
            entry = json.loads(open(src).read())
            attr = entry.get("Attributes")
            foundry = {
                        "_id": f"move-{entry['_id']}",
                        "name": entry['Name'],
                        "type": "move",
                        "img": "icons/svg/explosion.svg",
                        "system": {
                            "description": entry['Description'],
                            "yype": entry['Type'],
                            "category": entry['DmgType'],
                            "target": entry['Target'],
                            "power": entry['Power'],
                            "accMod1": entry['Accuracy1'],
                            "accMod2": entry['Accuracy2'],
                            "dmgMod": entry['Damage1'],
                            "effect": entry['Effect'],
                            "source": self.version,
                            "attributes": {
                                "accuracyReduction":   _attribute_get(attr, "AccuracyReduction"),
                                "priority":            _attribute_get(attr, "Priority"),
                                "highCritical":        _attribute_get(attr, "HighCritical"),
                                "lethal":              _attribute_get(attr, "Lethal"),
                                "physicalRanged":      _attribute_get(attr, "PhysicalRanged"),
                                "charge":              _attribute_get(attr, "Charge"),
                                "mustRecharge":        _attribute_get(attr, "MustRecharge"),
                                "fistBased":           _attribute_get(attr, "FistBased"),
                                "soundBased":          _attribute_get(attr, "SoundBased"),
                                "shieldMove":          _attribute_get(attr, "ShieldMove"),
                                "neverFail":           _attribute_get(attr, "NeverFail"),
                                "switcherMove":        _attribute_get(attr, "SwitcherMove"),
                                "recoil":              _attribute_get(attr, "Recoil"),
                                "rampage":             _attribute_get(attr, "Rampage"),
                                "doubleAction":        _attribute_get(attr, "DoubleAction"),
                                "alwaysCrit":          _attribute_get(attr, "AlwaysCrit"),
                                "destroyShield":       _attribute_get(attr, "DestroyShield"),
                                "successiveActions":   _attribute_get(attr, "SuccessiveActions"),
                                "userFaints":          _attribute_get(attr, "UserFaints"),
                                "resetTerrain":        _attribute_get(attr, "ResetTerrain"),
                                "resistedWithDefense": _attribute_get(attr, "ResistedWithDefense"),
                                "ignoreDefenses":      _attribute_get(attr, "IgnoreDefenses")
                            }
                        },
                        "effects": [],
                        "flags": {},
                        "folder": None,
                        "sort": 100001,
                        "_stats": {
                            "systemId": "pokerole",
                            "systemVersion": "1.2.0",
                            "coreVersion": "10.291",
                            "createdTime": 1670525752873,
                            "modifiedTime": datetime.datetime.now().timestamp(),
                            "lastModifiedBy": "Generator"
                        }
            }
            db.append(foundry)
        open(self.moves_output+f"Moves.json",'w').write(json.dumps(db))
    
    def _learnsets(self):
        pass
    
    def _natures(self):
        pass
    
    def _items(self):
        pass
            
    def _images(self):
        def x(path, output, postfix):
            for img in [x for x in os.listdir(path) if '.png' in x]:
                sname = img.split('.')
                Foundryname = f'Foundry-{sname[0]}-{postfix}.{sname[1]}'
                copy(path+img, output+Foundryname)
                # print(path+img, output+Foundryname)
        x(self.sprites_path, self.sprites_output, 'BoxSprite')
        x(self.home_path, self.home_output, 'HomeSprite')
        x(self.book_path, self.book_output, 'BookSprite')
        x(self.shuffle_path, self.shuffle_output, 'ShuffleToken')
        
def update(*argv, batch=False, version='Version20', confirm=False):
        
    foundry = Foundry(version)
    
    targets = {
        "pokedex":   foundry._pokedex,
        "abilities": foundry._abilities,
        "moves":     foundry._moves,
        "learnsets": foundry._learnsets,
        "natures":   foundry._natures,
        "items":     foundry._items,
        "images":    foundry._images
    }
    
    updates = list(targets.keys()) if batch else []
    for t in argv:
        if t.lower() in targets:
            updates.append(t.lower())
        else:
            print(f"WARN: Target {t.lower()} not configured, Skipping...")
    updates = set(updates)
    if not confirm: 
        conf = input(f'INFO: {updates}\nQUERY: Update these folders in Foundry? [Y/Yes]: ')
        if conf.lower() not in ['y', 'yes']:
            return "WARN: Did not confirm update, cancelling..."
    else: print(f'INFO: {updates}\nQUERY: Updating these folders in the Foundry...')
    
    for t in updates:
        func = targets[t]
        func()
        print(f'INFO: Folder {t} updated!')
        
    print('INFO: Foundry Update Complete.')
        
def help():
    print("""
    Python Script to update the Obsidian Foundry with the latest Data. 
    
    update: 
        update [collection names], [--batch] [--version Version] [--confirm] [--orphans [clear]] [--orphan_clear_confirm]
            collection names     : one or more of the folders in Foundry. Optional when using --batch.
            batch                : Optional. Updates all Foundry folderss
            version              : Optional. Changes the Version folder to be used in paths.
            confirm              : Optional. Skips confirmation step. 
    """)

if __name__ == '__main__':
  fire.Fire()