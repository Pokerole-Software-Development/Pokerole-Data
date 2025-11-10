from engine import Engine
from os.path import join, exists
from shutil import rmtree
from datetime import datetime
from hashlib import blake2b
import json

DEFAULT_POKEMON_MANEUVERS = ['Struggle', 'Grapple', 'Help Another', 'Cover an Ally', 'Run Away']
POKEMON_TOKEN_IMAGES = 'book'

class Foundry_Engine(Engine):
    
    def __init__(self, output_path, game_version, foundry_version):
        super().__init__(output_path, game_version)
        self.foundry_version = foundry_version
        self.display_version = f"Core {game_version}"
        # Wipe out the Output folder you provided. 
        rmtree(self.output_path, ignore_errors=True)
    
    # # These functions take JSON and return a string to be outputted. 
    
    def pokedex_entry(self, entry, write):
        learnset = entry["Moves"]
        moves = []
        abilities = []
        
        # Block where writes are disabled on the driver, to prevent adding
        # duplicate entries to the move/ability dbs
        self.driver._toggle_writes()
        for x in learnset:
            try:
                move = self.driver.generate_moves(file_match=f'{x["Name"]}.json')[0]
                move['system']['rank'] = x['Learned'].lower()
                moves.append(move)
            except IndexError as e:
                print(f"Move {x['Name']} not found in Pokemon {entry['Name']}")
                
        # For x in maneuvers
        
        for x in [entry['Ability1'], entry['Ability2']]:
            if not x: continue
            try:
                ability = self.driver.generate_abilities(file_match=f'{x}.json')[0]
                abilities.append(ability)
            except IndexError as e:
                print(f"Ability {x} not found in Pokemon {entry['Name']}")
        
        self.driver._toggle_writes()
    
        foundry_items = [json.dumps(x, ensure_ascii=False) for x in moves+abilities]
        
        foundry = {
            "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
            "name": entry['Name'],
            "type": "pokemon",
            "img": f"systems/pokerole/images/pokemon/{POKEMON_TOKEN_IMAGES}/{entry['Image']}",
            "system": {
                "hp": {
                    "value": entry['Vitality']+entry['BaseHP'], #leave it be regarding the new insight hp scalling optiona rule, it will recalculate on creation
                    "min": 0,
                    "max": entry['Vitality']+entry['BaseHP']
                },
                "will": {
                    "value": 3+entry['Insight'],
                    "min": 0,
                    "max": 3+entry['Insight']
                },
                "baseHp": entry['BaseHP'],
                "rank": "none",
                "recommendedRank": entry['RecommendedRank'].lower(),
                "personality": "hardy",
                "gender": "neutral", #new
                "actionCount": {
                "value": 0,
                "min": 0,
                "max": 5
                },
                "attributes": {
                "strength": {
                    "value": entry['Strength'],
                    "min": 0,
                    "max": entry['MaxStrength'],
                    "base": entry['Strength'] 
                },
                "dexterity": {
                    "value": entry['Dexterity'],
                    "min": 0,
                    "max": entry['MaxDexterity'],
                    "base": entry['Dexterity'] 
                },
                "vitality": {
                    "value": entry['Vitality'],
                    "min": 0,
                    "max": entry['MaxVitality'],
                    "base": entry['Vitality']
                },
                "special": {
                    "value": entry['Special'],
                    "min": 0,
                    "max": entry['MaxSpecial'],
                    "base": entry['Special']
                },
                "insight": {
                    "value": entry['Insight'],
                    "min": 0,
                    "max": entry['MaxInsight'],
                    "base": entry['Insight']
                },
                },
                "social": {
                "tough": {
                    "value": 1,
                    "min": 0,
                    "max": 5
                },
                "cool": {
                    "value": 1,
                    "min": 0,
                    "max": 5
                },
                "beauty": {
                    "value": 1,
                    "min": 0,
                    "max": 5
                },
                "cute": {
                    "value": 1,
                    "min": 0,
                    "max": 5
                },
                "clever": {
                    "value": 1,
                    "min": 0,
                    "max": 5
                }
                },
                "skills": {
                    "brawl": {
                        "value": 0,
                        "min": 0,
                        "max": 5
                    },
                    "channel": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "clash": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "evasion": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "alert": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "athletic": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "nature": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "stealth": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "charm": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "etiquette": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "intimidate": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    },
                    "perform": {
                    "value": 0,
                    "min": 0,
                    "max": 5
                    }
            },
                "biography": "",
                "battles": 0, 
                "trainingPoints": 0,
                "sheetskin": "skinOld",
                "pokedexId": entry['Number'],
                "species": entry['Name'],
                "pokedexCategory": entry['DexCategory'],
                "pokedexDescription": entry['DexDescription'],
                "type1": entry['Type1'].lower(),
                "type2": entry['Type2'].lower(),
                "type3": "none",
                "hasThirdType": False,
                "height": entry['Height']['Meters'],
                "weight": entry['Weight']['Kilograms'],
                "extra": {
                "happiness": {
                    "value": 2,
                    "min": 0,
                    "max": 5
                },
                "loyalty": {
                    "value": 2,
                    "min": 0,
                    "max": 5
                }
                },
                "source": self.display_version,
            },
            "prototypeToken": {
                "name": entry['Name'],
                "displayName": 0,
                "actorLink": False,
                "texture": {
                "src": f"systems/pokerole/images/pokemon/{POKEMON_TOKEN_IMAGES}/{entry['Image']}",
                "scaleX": 1,
                "scaleY": 1,
                "offsetX": 0,
                "offsetY": 0,
                "rotation": 0,
                "tint": None
                },
                "width": 1,
                "height": 1,
                "lockRotation": False,
                "rotation": 0,
                "alpha": 1,
                "disposition": -1,
                "displayBars": 0,
                "bar1": {
                "attribute": "hp"
                },
                "bar2": {
                "attribute": "will"
                },
                "light": {
                "alpha": 0.5,
                "angle": 360,
                "bright": 0,
                "color": None,
                "coloration": 1,
                "dim": 0,
                "attenuation": 0.5,
                "luminosity": 0.5,
                "saturation": 0,
                "contrast": 0,
                "shadows": 0,
                "animation": {
                    "type": None,
                    "speed": 5,
                    "intensity": 5,
                    "reverse": False
                },
                "darkness": {
                    "min": 0,
                    "max": 1
                }
                },
                "sight": {
                "enabled": False,
                "range": None,
                "angle": 360,
                "visionMode": "basic",
                "color": None,
                "attenuation": 0.1,
                "brightness": 0,
                "saturation": 0,
                "contrast": 0
                },
                "detectionModes": [],
                "flags": {},
                "randomImg": False,
            },
            "items": foundry_items,
            "effects": [],
            "flags": {},
            "_stats": {
                "systemId": "pokerole",
                "systemVersion": self.game_version,
                "coreVersion": self.foundry_version,
                "createdTime": 1670952558737,
                "modifiedTime": datetime.now().timestamp(),
                "lastModifiedBy": "Generator"
            }
        }
        if write:
            path = join(self.output_path,'packs', 'pokedex.db')
            self._write_to(json.dumps(foundry, ensure_ascii=False)+'\n', path, "a")
        return foundry
        
    def movedex_entry(self, entry, write=True):

        def _icon_for_type(type):
            if type == 'none':
                # TODO: is there anything better than Normal for typeless moves?
                return 'systems/pokerole/images/types/normal.svg'
            
            return f'systems/pokerole/images/types/{type}.svg'

        def _convert_heal_data(data):
            converted = { 'type': 'none' }
            if not data: return converted
            
            ty = data.get('Type')
            target = data.get('Target')
            will_point_cost = data.get('WillPointCost')
            percentage = data.get('Percentage')
            if not ty or not target:
                raise 'Type or target missing in heal data'

            if ty:
                converted['type'] = ty.lower()
            if target:
                converted['target'] = target.lower()
            converted['willPointCost'] = will_point_cost if will_point_cost else 0
            if percentage:
                converted['amount'] = percentage
            return converted
        
        attr = entry.get("Attributes", {})
        id = entry['_id']

        accAttr1 = entry['Accuracy1'].lower()
        if '/' in accAttr1:
            accAttr1, accAttr2 = accAttr1.split('/')
        else: accAttr2 = ""
        accSkill1 = entry['Accuracy2'].lower()
        if '/' in accSkill1:
            accSkill1, accSkill2 = accSkill1.split('/')
        else: accSkill2 = ""
        dmgMod1 = entry['Damage1'].lower()
        if '/' in dmgMod1:
            dmgMod1, dmgMod2 = dmgMod1.split('/')
        else: dmgMod2 = ""
        move_type = entry['Type'].lower()
        description = entry['Description']
        effect = entry['Effect']

        # Remove empty added effects
        if effect == '-':
            effect = ''

        if move_type == "typeless":
            move_type = "none"

        # Special cases that can't be rolled automatically
        # if id == 'lovely-kiss':
        #     accAttr1 = ''
        #     accSkill1 = ''
        #     effect += ' Roll (5 - Beauty) + Allure dice for accuracy.'
        # if id == 'copycat':
        #     accAttr1 = ''
        #     accSkill1 = ''
        #     dmgMod1 = ''
        #     effect += ' Use the same dice pool for accuracy and damage.'
        # if id == 'help-another':
        #     accAttr1 = ''
        #     accSkill1 = ''
        
        foundry = {
            "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
            "name": entry['Name'],
            "type": "move",
            "img": _icon_for_type(move_type),
            "system": {
                "description": description,
                "type": move_type,
                "category": entry['Category'].lower(),
                # Special case for Spider Web (Really?)
                "target": entry['Target'],
                "power": entry['Power'],
                "accAttr1": accAttr1,
                "accAttr1var": accAttr2,
                "accSkill1": accSkill1,
                "accSkill1var": accSkill2,
                "dmgMod1": dmgMod1,
                "dmgMod1var": dmgMod2,
                "effect": effect,
                "source": self.display_version,
                "attributes": { #characteristics where left the same but if there is a new one from the manual add it without hesitation for future improvements :D i will figure out something!
                    "accuracyReduction":   attr.get("AccuracyReduction", 0),
                    "priority":            attr.get("Priority", 0),
                    "highCritical":        attr.get("HighCritical", False),
                    "lethal":              attr.get("Lethal", False),
                    "physicalRanged":      attr.get("PhysicalRanged", False),
                    "charge":              attr.get("Charge", False),
                    "mustRecharge":        attr.get("MustRecharge", False),
                    "fistBased":           attr.get("FistBased", False),
                    "soundBased":          attr.get("SoundBased", False),
                    "shieldMove":          attr.get("ShieldMove", False),
                    "neverFail":           attr.get("NeverFail", False),
                    "switcherMove":        attr.get("SwitcherMove", False),
                    "recoil":              attr.get("Recoil", False),
                    "rampage":             attr.get("Rampage", False),
                    "doubleAction":        attr.get("DoubleAction", False),
                    "alwaysCrit":          attr.get("AlwaysCrit", False),
                    "destroyShield":       attr.get("DestroyShield", False),
                    "successiveActions":   attr.get("SuccessiveActions", False),
                    "userFaints":          attr.get("UserFaints", False),
                    "resetTerrain":        attr.get("ResetTerrain", False),
                    "resistedWithDefense": attr.get("ResistedWithDefense", False),
                    "ignoreDefenses":      attr.get("IgnoreDefenses", False),
                    "maneuver":            move_type == "none"
                },
                "heal": _convert_heal_data(entry.get('AddedEffects',{}).get('Heal', {})),
            },
            "effects": [], #No changes on effects or Added Effects so all good
            "flags": {},
            "folder": None,
            "sort": 100001,
            "_stats": {
                "systemId": "pokerole",
                "systemVersion": self.game_version,
                "coreVersion": self.foundry_version,
                "createdTime": 1670525752873,
                "modifiedTime": datetime.now().timestamp(),
                "lastModifiedBy": "Generator"
            }
        }
        if write:
            path = join(self.output_path,'packs', 'moves.db')
            self._write_to(json.dumps(foundry, ensure_ascii=False)+'\n', path, "a")
        return foundry
        
    def abilitydex_entry(self, entry, write=True):
        foundry = {
            "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
            "name": entry['Name'],
            "type": "ability",
            "img": "icons/svg/book.svg",
            "system": {
                "description": f"<p>{entry['Effect']}</p><p>{entry['Description']}</p>"
            },
            "effects": [],
            "source": self.display_version,
            "flags": {},
            "_stats": {
                "systemId": "pokerole",
                "systemVersion": self.game_version,
                "coreVersion": self.foundry_version,
                "createdTime": 1670695293664,
                "modifiedTime": datetime.now().timestamp(),
                "lastModifiedBy": "Generator"
            }
        }
        if write:
            path = join(self.output_path,'packs', 'abilities.db')
            self._write_to(json.dumps(foundry, ensure_ascii=False)+'\n', path, "a")

        return foundry
    
    def itemdex_entry(self, entry, write=True):
        # Add the price if it's numeric
        price = entry.get('TrainerPrice')
        if price:
            try:
                price = int(price)
            except ValueError:
                price = None

        img = f"systems/pokerole/images/items/{entry['_id']}.png"
        if not exists(f"../../images/ItemSprites/{entry['_id']}.png"):
            img = "icons/svg/item-bag.svg"
        foundry = {
            "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
            "name": entry['Name'],
            "type": "item",
            "img": img,
            "system": {
                "description": f"<p>{entry['Description']}</p>",
                "price": price,
                "pocket": "item" # For the Auto-sort inventory function on live!
                #We can discuss about it, have a list of "pockets" implemented but maybe is better to build a list by ourselves and clasify the items at database level
            },
            "effects": [],
            "source": entry["Source"],
            "flags": {},
            "_stats": {
                "systemId": "pokerole",
                "systemVersion": self.game_version,
                "coreVersion": self.foundry_version,
                "createdTime": 1670695293664,
                "modifiedTime": datetime.now().timestamp(),
                "lastModifiedBy": "Generator"
            }
        }
        if write:
            path = join(self.output_path,'packs', 'items.db')
            self._write_to(json.dumps(foundry, ensure_ascii=False)+'\n', path, "a")

        return foundry
    
    def import_images(self, source, setname):
        fndry_folder = {'BookSprites':'book', 'HomeSprites':'home', 'BoxSprites':'box', 'ShuffleTokens':'shuffle', "ItemSprites":'items'}[setname]
        target_path = join(self.output_path, join('images', fndry_folder))
        self._pathgen(target_path)
        self._copy_imageset(source, target_path)