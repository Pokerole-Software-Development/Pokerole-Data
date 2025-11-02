from DataBuilder import DataBuilder
from fire import Fire
from glob import glob
from os.path import join
from os import listdir
from shutil import copy, rmtree
import json
import os
import datetime
from hashlib import blake2b

# secrets = json.load(open('../../secrets.json'))

# System version used if the `--system_version` flag is not specified
DEFAULT_FOUNDRY_SYSTEM_VERSION = "0.3.1"

# Moves with fields that are problematic for the export
# - Any Move is too generic, individual moves can be added to Mew instead
# - Struggle, Growl and Photon Geyser have attributes like "Strength/special", but there are specialized versions for each attribute
IGNORED_MOVES = ['any-move', 'struggle', 'growl', 'photon-geyser']

# Stabilize An Ally is usually only used by trainers (Pokémon don't have the Medicine skill)
DEFAULT_POKEMON_MANEUVERS = ['Struggle (Physical)', 'Struggle (Special)', 'Grapple', 'Help Another', 'Cover an Ally', 'Run Away']

# Remapping of ailments from the dataset to the Foundry system
AILMENT_REMAPPING = {
    "Fainted": "fainted",
    "Paralyze": "paralysis",
    "Freeze": "frozen",
    "Poison": "poison",
    "BadlyPoison": "badlyPoisoned",
    "Sleep": "sleep",
    "Burn": "burn1",
    "Burn1": "burn1",
    "Burn2": "burn2",
    "Burn3": "burn3",
    "Flinch": "flinch",
    "Confuse": "confused",
    "Disable": "disabled",
    "Infaturate": "infatuated",
}

class Foundry_DataBuilder(DataBuilder):
    """
    This object takes the Pokerole Dataset and Builds it as Foundry compatable data. 
    
    :param root: Base directory of your Dataset.
    :param pokerole_version: Version of the Pokerole system to use. Same as the folder name.
    :param system_version: Foundry's system version 
    :param foundry_dir: The path to the Data/systems/pokerole folder in your foundry installatiomn.
    """
    
    def __init__(self, 
                root='../',
                pokerole_version='v3.0',
                system_version='0.3.1',
                # foundry_dir='/Users/bill/Library/Application Support/FoundryVTT/Data/systems/pokerole'
                foundry_dir='/Volumes/Files/RPG Assets/Foundry/Data/systems/pokerole'
                # foundry_dir='/Users/admin/repos/foundry-pokerole'
                ):
        super().__init__(root, pokerole_version)
        self.system_version = system_version
        self.foundry_dir = foundry_dir
        self.display_version = f"Core {pokerole_version}"

    def _fndry_path_prep(self, source, output):
        path = self._pathgen(source)
        outpath = self._pathgen(output, root=self.foundry_dir, does_exist=False)
        return path, outpath

    def build_pokedex(
            self, 
            source='{version}/Pokedex',
            output='packs',
            sheet_img='book', 
            token_img='book'):
        """
        Builds the Pokedex. Leverages Moves and Abilities to do so.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        :param sheet_img: What Image source to use for the Sheet Image. Either 'book', 'box', 'home', or 'shuffle'.
        :param token_img: What Image source to use for the Token Image. Either 'book', 'box', 'home', or 'shuffle'.
        """
        pokedex_path, pokedex_output = self._fndry_path_prep(source, output)
        sheet_img = sheet_img.lower() if sheet_img.lower() in ['book', 'box', 'home', 'shuffle'] else 'book'
        token_img = token_img.lower() if token_img.lower() in ['book', 'box', 'home', 'shuffle'] else 'book'
        db = []
        try:
            for src in glob(pokedex_path+"/*.json"):
                entry = json.loads(open(src).read())
                
                learnset = entry["Moves"]
                moves = []
                ranks = []
                for x in learnset:
                    if x['Name'] == "Growl": # Use the two versions of Growl since it would otherwise be skipped over
                        moves.append('Growl (Tough)')
                        ranks.append(x['Learned'])
                        moves.append('Growl (Cute)')
                        ranks.append(x['Learned'])
                    elif x['Name'] == "Photon Geyser":
                        moves.append('Photon Geyser (Physical)')
                        ranks.append(x['Learned'])
                        moves.append('Photon Geyser (Special)')
                        ranks.append(x['Learned'])
                    else:
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
        except:
            print(src, entry, moves, ranks)
            raise
        rmtree(join(pokedex_output, "pokedex"),ignore_errors=True)
        with open(join(pokedex_output, "pokedex.db"),'w') as f:
            for x in db:
                f.write(json.dumps(x)+'\n')
    
    def build_abilities(
            self, 
            source='{version}/Abilities', 
            output='packs', 
            alist=None):
        """
        Builds the Ability Dex.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        :param alist: A list of abilities to generate data for. Used by the Pokedex Build.
        """
        abilities_path, abilities_output = self._fndry_path_prep(source, output)
        db = []
        iter_target = glob(abilities_path+"/*.json") if not alist else [f"{abilities_path}/{x}.json" for x in alist if x]
        for src in iter_target:
            try:
                entry = json.loads(open(src).read())
            except FileNotFoundError as e:
                if alist: 
                    print(f"ERROR: Ability {src} not found.")
                    continue
                else: raise e

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
                    "systemVersion": self.system_version,
                    "coreVersion": "10.291",
                    "createdTime": 1670695293664,
                    "modifiedTime": datetime.datetime.now().timestamp(),
                    "lastModifiedBy": "Generator"
                }
            }

            db.append(foundry)
        if not alist:
            rmtree(join(abilities_output, "abilities"),ignore_errors=True)
            with open(join(abilities_output, "abilities.db"),'w') as f:
                for x in db:
                    f.write(json.dumps(x)+'\n')
        return db
    
    def build_moves(
            self, 
            source='{version}/Moves',
            output='packs',
            mlist=False, 
            ranks=False):
        """
        Builds the Move Dex.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        :param mlist: A list of Moves to generate data for. Used by the Pokedex Build.
        :param ranks: A list of ranks that are linked to the Moves in the mlist. 
        Used by the Pokedex Build.
        """
        def _attribute_get(attr, value, default=False):
            if not attr: return default
            else: return attr.get(value) if attr.get(value) else default

        def _icon_for_type(type):
            if type == 'none':
                # TODO: is there anything better than Normal for typeless moves?
                return 'systems/pokerole/images/types/normal.svg'
            
            return f'systems/pokerole/images/types/{type}.svg'

        def _check_target(target):
            assert target in ["Foe", "Random Foe", "All Foes", "User", "One Ally", "User and Allies",
                "Area", "Battlefield", "Battlefield (Foes)", "Battlefield and Area", "All Allies"], f"Invalid target '{target}'"

        def _check_attribute(attr):
            assert attr in ["strength", "dexterity", "vitality", "special", "insight", "tough", "cool", "beauty", "cute", "clever", "will"], f"Invalid attribute '{attr}'"

        def _check_skill(attr):
            assert attr in ["brawl", "channel", "clash", "evasion", "alert", "athletic", "nature", "stealth", "allure", "etiquette", "intimidate", "perform", "crafts", "lore", "medicine", "science", "empathy", "throw"], f"Invalid attribute '{attr}'"

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
        
        # Convert from PascalCase to camelCase
        def _pascal_to_camel(s):
            if not s: return s
            return s[0].lower() + s[1:]  # Convert the first letter to lowercase
        
        def _convert_effect_groups(added_effects):
            effect_groups = []
            unconditional_ailments = []

            # Handle ailments
            for ailment in added_effects.get("Ailments", []):
                ailment_type = AILMENT_REMAPPING.get(ailment["Type"])
                # Skip unsupported ailments
                if not ailment_type:
                    continue

                chance_dice = ailment.get("ChanceDice")
                if chance_dice:
                    # Conditional ailments
                    condition = {"type": "chanceDice", "amount": chance_dice}
                    effect_group = {
                        "condition": condition,
                        "effects": [
                            {
                                "type": "ailment",
                                "ailment": ailment_type,
                                "affects": ailment["Affects"].lower()
                            }
                        ]
                    }
                    effect_groups.append(effect_group)
                else:
                    # Unconditional ailments
                    unconditional_ailments.append({
                        "type": "ailment",
                        "ailment": ailment_type,
                        "affects": ailment["Affects"].lower()
                    })

            # Group all unconditional ailments together
            if unconditional_ailments:
                effect_groups.append({
                    "condition": {"type": "none"},
                    "effects": unconditional_ailments
                })

            # Handle stat changes
            for stat_change in added_effects.get("StatChanges", []):
                chance_dice = stat_change.get("ChanceDice")
                condition = {"type": "chanceDice", "amount": chance_dice} if chance_dice else {"type": "none"}

                effects = []
                for stat in stat_change.get("Stats", []):
                    stat = _pascal_to_camel(stat)
                    if stat == "accuracy":
                        stat = "accuracyMod"

                    effects.append({
                        "type": "statChange",
                        "stat": stat,
                        "amount": stat_change["Stages"],
                        "affects": stat_change["Affects"].lower()
                    })

                effect_group = {
                    "condition": condition,
                    "effects": effects
                }
                effect_groups.append(effect_group)

            return effect_groups
        
        moves_path, moves_output = self._fndry_path_prep(source, output)
        db = []
        iter_target = glob(moves_path+"/*.json") if not mlist else [f"{moves_path}/{x}.json" for x in mlist]
        for src in iter_target:
            try:
                entry = json.loads(open(src).read())
            except FileNotFoundError as e:
                if mlist: 
                    print(f"ERROR: move {src} not found.")
                    continue
                else: raise e
            # except Exception as e:
            #     print("Exception in Moves")
            #     print(iter_target)
            #     print(src)
            #     raise e
            attr = entry.get("Attributes")
            id = entry['_id']

            if id in IGNORED_MOVES:
                continue
            if '/' in entry['Accuracy1'].lower(): continue
            if '/' in entry['Accuracy2'].lower(): continue

            accMod1 = entry['Accuracy1'].lower()
            accMod2 = entry['Accuracy2'].lower()
            dmgMod = entry['Damage1'].lower()
            move_type = entry['Type'].lower()
            description = entry['Description']
            effect = entry['Effect']

            # Remove empty added effects
            if effect == '-':
                effect = ''

            if move_type == "typeless":
                move_type = "none"

            # Special cases that can't be rolled automatically
            if id == 'lovely-kiss':
                accMod1 = ''
                accMod2 = ''
                effect += ' Roll (5 - Beauty) + Allure dice for accuracy.'
            if id == 'simple-beam':
                accMod1 = ''
                accMod2 = ''
                effect += ' Roll Insight+Empathy dice for accuracy. See the description for more details.'
                description += "<p>Empathy is a custom skill, which you can add manually on the Pokémon's character sheet. You can edit this move to auto-roll once you've added the skill by setting Accuracy Modifier 1 to 'insight' and Accuracy Modifier 2 to 'empathy'.</p>"
            if id == 'copycat':
                accMod1 = ''
                accMod2 = ''
                dmgMod = ''
                effect += ' Use the same dice pool for accuracy and damage.'
            if id == 'help-another':
                accMod1 = ''
                accMod2 = ''

            # Data consistency checks
            _check_target(entry['Target'])
            if accMod1 != '':
                _check_attribute(accMod1)
            if accMod2 != '':
                _check_skill(accMod2)
            if dmgMod != '':
                _check_attribute(dmgMod)

            effect_groups = _convert_effect_groups(entry.get("AddedEffects", {}))

            foundry = {
                        "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
                        "name": entry['Name'],
                        "type": "move",
                        "img": _icon_for_type(move_type),
                        "system": {
                            "description": description,
                            "type": move_type,
                            "category": entry['Category'].lower(),
                            # Special case for Spider Web
                            "target": entry['Target'] if id != 'spider-web' else "Battlefield (Foes)",
                            "power": entry['Power'],
                            "accMod1": accMod1,
                            "accMod2": accMod2,
                            "dmgMod": dmgMod,
                            "effect": effect,
                            "effectGroups": effect_groups,
                            "source": self.display_version,
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
                                "ignoreDefenses":      _attribute_get(attr, "IgnoreDefenses"),
                                "maneuver":            move_type == "none"
                            },
                            "heal": _convert_heal_data(entry['AddedEffects'].get('Heal')),
                        },
                        "effects": [],
                        "flags": {},
                        "folder": None,
                        "sort": 100001,
                        "_stats": {
                            "systemId": "pokerole",
                            "systemVersion": self.system_version,
                            "coreVersion": "10.291",
                            "createdTime": 1670525752873,
                            "modifiedTime": datetime.datetime.now().timestamp(),
                            "lastModifiedBy": "Generator"
                        }
            }
            if ranks and len(ranks) == len(iter_target):
                foundry['system']['rank'] = ranks[iter_target.index(src)].lower()
            db.append(foundry)
        if not mlist:
            rmtree(join(moves_output, "moves"),ignore_errors=True)
            with open(join(moves_output, "moves.db"),'w') as f:
                for x in db:
                    f.write(json.dumps(x)+'\n')
        return db
    
    def build_items(
            self, 
            source='{version}/Items', 
            output='packs'
            ):
        """
        Builds the Item Dex.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        db = []
        items_path, items_output = self._fndry_path_prep(source, output)

        for src in glob(items_path+"/*.json"):
            entry = json.loads(open(src).read())

            # Add the price if it's numeric
            price = entry.get('TrainerPrice')
            if price:
                try:
                    price = int(price)
                except ValueError:
                    price = None

            img = f"systems/pokerole/images/items/{entry['_id']}.png"
            if not os.path.exists(f"../images/ItemSprites/{entry['_id']}.png"):
                img = "icons/svg/item-bag.svg"

            foundry = {
                "_id": blake2b(bytes(entry['_id'], 'utf-8'), digest_size=16).hexdigest(),
                "name": entry['Name'],
                "type": "item",
                "img": img,
                "system": {
                    "description": f"<p>{entry['Description']}</p>",
                    "price": price,
                },
                "effects": [],
                "source": entry["Source"],
                "flags": {},
                "_stats": {
                    "systemId": "pokerole",
                    "systemVersion": self.system_version,
                    "coreVersion": "10.291",
                    "createdTime": 1670695293664,
                    "modifiedTime": datetime.datetime.now().timestamp(),
                    "lastModifiedBy": "Generator"
                }
            }
            db.append(foundry)
        
        rmtree(join(items_output, "items"),ignore_errors=True)
        with open(join(items_output, "items.db"),'w') as f:
            for x in db:
                f.write(json.dumps(x)+'\n')
    
    def _copy_imageset(self, source, output):
        for img in [x for x in listdir(source) if '.png' in x]:
            # sname = img.split('.')
            # srdname = f'{sname[0]}.{sname[1]}'
            copy(join(source, img), join(output, img))
            # print(join(source, img), join(output, srdname))

    def build_boxsprites(self, source="images/BoxSprites", output='images/pokemon/box'):
        """
        Copies the Box Sprites into Foundry.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        inpath, outpath = self._fndry_path_prep(source, output)
        self._copy_imageset(inpath, outpath)
        
    def build_homesprites(self, source="images/HomeSprites", output='images/pokemon/home'):
        """
        Copies the Home Sprites into Foundry.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        inpath, outpath = self._fndry_path_prep(source, output)
        self._copy_imageset(inpath, outpath)

    def build_booksprites(self, source="images/BookSprites", output='images/pokemon/book'):
        """
        Copies the Book Sprites into Foundry.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        inpath, outpath = self._fndry_path_prep(source, output)
        self._copy_imageset(inpath, outpath)

    def build_shuffletokens(self, source="images/ShuffleTokens", output='images/pokemon/shuffle'):
        """
        Copies the Shuffle Sprites into Foundry.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        inpath, outpath = self._fndry_path_prep(source, output)
        self._copy_imageset(inpath, outpath)

    def build_itemsprites(self, source="images/ItemSprites", output='images/items'):
        """
        Copies the Item Sprites into Foundry.
        
        If `{version}` is in either source or output, it will replaced 
        with the pokerole_version provided on object creation.
        
        :param source: Directory to load data from. Should be within the root class parameter.
        :param output: Directory to save data to. Should be within the root class parameter.
        """
        inpath, outpath = self._fndry_path_prep(source, output)
        self._copy_imageset(inpath, outpath)
    
    # def _build_images(self, source="", output=''):
    #     """
    #     Function to trigger all the image builds with one shortcut. 
    #     Cannot accept parameters for each, they use defaults only.
    #     """
    #     self.build_booksprites()
    #     self.build_boxsprites()
    #     self.build_homesprites()
    #     self.build_shuffletokens()
    #     self.build_itemsprites()
        
    def help(self):
        print("""
        Python Script to update the Obsidian Foundry with the latest Data. 
        
        update: 
            update [collection names], [--batch] [--system_version] Version [--version Version] [--confirm] [--sheet_images src] [--token_images src]
                collection names     : one or more of the folders in Foundry. Optional when using --batch.
                batch                : Optional. Updates all Foundry folders.
                system_version       : Optional. The target Foundry system version.
                version              : Optional. Changes the Version folder to be used in paths.
                confirm              : Optional. Skips confirmation step. 
                sheet_images         : Optional. Source of pokemon sheet images. Either 'book', 'home', 'box', or 'shuffle'.
                token_images         : Optional. Source of pokemon token images. Either 'book', 'home', 'box', or 'shuffle'.
        """)

if __name__ == '__main__':
    Fire(Foundry_DataBuilder)
