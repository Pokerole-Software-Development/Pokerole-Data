from glob import glob
import json
import os
from shutil import copy
import fire
import datetime

# Moves with fields that are problematic for the export
# - Non-moves such as "Run Away" are excluded
# - Struggle and Growl have attributes like "Strength/special"
# - Copycat Damage1 is "Same as the copied move"
# - Simple Beam is rolled with Empathy. This skill exists neither on the Pokémon sheet nor on the trainer sheet (?)
# - Lovely Kiss Accuracy1 is "Missing beauty"
IGNORED_MOVES = ['any-move', 'struggle', 'grapple', 'help-another', 'cover-an-ally', 'stabilize-an-ally', 'run-away', 'copycat', 'simple-beam', 'growl', 'lovely-kiss']

class Foundry(object):
    
    def __init__(self, version="Version20"):
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
            
        self.pokedex_output = '../../Foundry/packs/'
        self.abilities_output = '../../Foundry/packs/'
        self.moves_output = '../../Foundry/packs/'
        self.learnsets_output = '../../Foundry/packs/'
        self.natures_output = '../../Foundry/packs/'
        self.sprites_output = '../../Foundry/images/pokemon/box/'
        self.home_output = '../../Foundry/images/pokemon/home/'
        self.book_output = '../../Foundry/images/pokemon/book/'
        self.shuffle_output = '../../Foundry/images/pokemon/shuffle/'
        self.items_output = '../../Foundry/packs/'

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
        
        def _attribute_get(attr, value, default=False):
            if not attr: return default
            else: return attr.get(value) if attr.get(value) else default

        def _icon_for_category(dmg_type):
            # TODO: Improve move icons
            # Maybe a combination of type + category since icons for every single move aren't feasible?
            img = "icons/svg/explosion.svg"
            if dmg_type == "Special":
                img = "icons/svg/daze.svg"
            elif dmg_type == "Support":
                img = "icons/svg/mage-shield.svg"
            return img

        def _check_target(target):
            assert target in ["Foe","Random Foe","All Foes","User","One Ally","User and Allies",
                "Area","Battlefield","Battlefield (Foes)", "Battlefield and Area"], f"Invalid target '{target}'"

        def _check_attribute(attr):
            assert attr in ["strength", "dexterity", "vitality", "special", "insight", "tough", "cool", "beauty", "cute", "clever", "will"], f"Invalid attribute '{attr}'"

        def _check_skill(attr):
            assert attr in ["brawl", "channel", "clash", "evasion", "alert", "athletic", "nature", "stealth", "allure", "etiquette", "intimidate", "perform", "crafts", "lore", "medicine", "science"], f"Invalid attribute '{attr}'"
        
        db = open(self.moves_output+"moves.db",'w')
        for src in glob(self.moves_path+"/*.json"):
            entry = json.loads(open(src).read())
            attr = entry.get("Attributes")

            if entry['_id'] in IGNORED_MOVES:
                continue

            _check_target(entry['Target'])
            if entry['Accuracy1'] != '':
                _check_attribute(entry['Accuracy1'].lower())
            if entry['Accuracy2'] != '':
                _check_skill(entry['Accuracy2'].lower())
            if entry['Damage1'] != '':
                _check_attribute(entry['Damage1'].lower())

            foundry = {
                        "_id": f"move-{entry['_id']}",
                        "name": entry['Name'],
                        "type": "move",
                        "img": _icon_for_category(entry['DmgType']),
                        "system": {
                            "description": entry['Description'],
                            "type": entry['Type'].lower(),
                            "category": entry['DmgType'].lower(),
                            # Special case for Spider Web
                            "target": entry['Target'] if entry['_id'] != 'spider-web' else "Battlefield (Foes)",
                            "power": entry['Power'],
                            "accMod1": entry['Accuracy1'].lower(),
                            "accMod2": entry['Accuracy2'].lower(),
                            "dmgMod": entry['Damage1'].lower(),
                            "effect": entry['Effect'],
                            "source": self.version,
                            "attributes": {
                                "accuracyReduction":   _attribute_get(attr, "AccuracyReduction", 0),
                                "priority":            _attribute_get(attr, "Priority", 0),
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
                            "systemVersion": "0.1.0",
                            "coreVersion": "10.291",
                            "createdTime": 1670525752873,
                            "modifiedTime": datetime.datetime.now().timestamp(),
                            "lastModifiedBy": "Generator"
                        }
            }
            db.write(json.dumps(foundry))
            db.write('\n')
        db.close()
    
    def _learnsets(self):
        pass
    
    def _natures(self):
        pass
    
    def _items(self):
        pass
            
    def _images(self):
        def x(path, output):
            for img in [x for x in os.listdir(path) if '.png' in x]:
                copy(path+img, output+img)
        x(self.sprites_path, self.sprites_output)
        x(self.home_path, self.home_output)
        x(self.book_path, self.book_output)
        x(self.shuffle_path, self.shuffle_output)
        
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
