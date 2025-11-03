from os.path import join, exists
from os import makedirs
from fire import Fire

DEFAULT_POKEMON_MANEUVERS = ['Struggle', 'Grapple', 'Help Another', 'Cover an Ally', 'Run Away']

class Engine(object):
    
    def __init__(self, output_path, game_version, foundry_version):
        super().__init__(output_path, game_version)
        self.foundry_version = foundry_version
        self.display_version = f"Core {game_version}"
    
    # # These functions take JSON and return a string to be outputted. 
    
    def pokedex_entry(self, entry):
        learnset = entry["Moves"]
        moves = []
        ranks = []
        for x in learnset:
            moves.append(x['Name'])
            ranks.append(x['Learned'])

        moves += DEFAULT_POKEMON_MANEUVERS
        ranks += ['starter'] * len(DEFAULT_POKEMON_MANEUVERS)
        move_list = self.build_moves(mlist=moves, ranks=ranks)

        abilities = self.build_abilities(alist=[entry['Ability1'], entry['Ability2']])
        hidden_ability_list = self.build_abilities(alist=[entry['HiddenAbility']])
        if len(hidden_ability_list) > 0:
            ability = hidden_ability_list[0]
            ability["name"] += " [Hidden Ability]"
            abilities.append(ability)
        event_ability_list = self.build_abilities(alist=[entry['EventAbilities']])
        if len(event_ability_list) > 0:
            ability = event_ability_list[0]
            ability["name"] += " [Event]"
            abilities.append(ability)

        foundry_items = move_list+abilities
        
        foundry = {
                    "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
                    "name": entry['Name'],
                    "type": "pokemon",
                    "img": f"systems/pokerole/images/pokemon/{sheet_img}/{entry['Image']}",
                    "system": {
                        "hp": {
                            "value": entry['Vitality']+entry['BaseHP'],
                            "min": 0,
                            "max": entry['Vitality']+entry['BaseHP']
                        },
                        "will": {
                            "value": 2+entry['Insight'],
                            "min": 0,
                            "max": 2+entry['Insight']
                        },
                        "baseHp": entry['BaseHP'],
                        "rank": "none",
                        "recommendedRank": entry['RecommendedRank'].lower(),
                        # Nature is named "personality" internally to avoid conflicts with the "Nature" skill
                        "personality": "hardy",
                        "confidence": 0,
                        "attributes": {
                        "strength": {
                            "value": entry['Strength'],
                            "min": 0,
                            "max": entry['MaxStrength']
                        },
                        "dexterity": {
                            "value": entry['Dexterity'],
                            "min": 0,
                            "max": entry['MaxDexterity']
                        },
                        "vitality": {
                            "value": entry['Vitality'],
                            "min": 0,
                            "max": entry['MaxVitality']
                        },
                        "special": {
                            "value": entry['Special'],
                            "min": 0,
                            "max": entry['MaxSpecial']
                        },
                        "insight": {
                            "value": entry['Insight'],
                            "min": 0,
                            "max": entry['MaxInsight']
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
                            "min": 0
                        },
                        "evasion": {
                            "value": 0,
                            "min": 0
                        },
                        "alert": {
                            "value": 0,
                            "min": 0
                        },
                        "athletic": {
                            "value": 0,
                            "min": 0
                        },
                        "nature": {
                            "value": 0,
                            "min": 0
                        },
                        "stealth": {
                            "value": 0,
                            "min": 0
                        },
                        "allure": {
                            "value": 0,
                            "min": 0
                        },
                        "etiquette": {
                            "value": 0,
                            "min": 0
                        },
                        "intimidate": {
                            "value": 0,
                            "min": 0
                        },
                        "perform": {
                            "value": 0,
                            "min": 0
                        },
                        "channel": {
                            "value": 0,
                            "min": 0
                        },
                        "clash": {
                            "value": 0,
                            "min": 0
                        }
                        },
                        "biography": "",
                        "battles": 0,
                        "victories": 0,
                        "pokedexId": entry['Number'],
                        "species": entry['Name'],
                        "pokedexCategory": entry['DexCategory'],
                        "pokedexDescription": entry['DexDescription'],
                        "type1": entry['Type1'].lower(),
                        "type2": entry['Type2'].lower(),
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
                        "src": f"systems/pokerole/images/pokemon/{token_img}/{entry['Image']}",
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
                        "systemVersion": self.system_version,
                        "coreVersion": "10.291",
                        "createdTime": 1670952558737,
                        "modifiedTime": datetime.datetime.now().timestamp(),
                        "lastModifiedBy": "Generator"
                    }
                    }
        db.append(foundry)
        
    def movedex_entry(self, entry):
        pass
    def abilitydex_entry(self, entry):
        pass
    def itemdex_entry(self, entry):
        pass
