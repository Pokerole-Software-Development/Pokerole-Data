import yaml
from glob import glob
import json
import os
import pandas as pd
import re
from shutil import copy
import fire
import time

secrets = json.load(open('../../secrets.json'))

# Pokedex template is in the function, needs access to variable during iteration. 

ability_template = '''## `= this.name`

> *`= this.Description`*

**Effect:** `= this.Effect`'''

#-------------------------------------------------------------

moves_template = '''### `= this.name` 
*`= this.Description`*

**Accuracy:** `= this.Accuracy1` + `= this.Accuracy2`
**Damage:** `= this.Power` `= choice(length(this.Damage1)=0, "","\+ "+ this.Damage1)` `= choice(length(this.Damage2)=0, "","\+ "+ this.Damage2)`

| Type          | Target          | Damage Type          | Power          |
| ------------- | --------------- | ---------------- | -------------- |
| `= this.Type` | `= this.Target` | `= this.DmgType` | `= this.Power` | 

**Effect:** `= this.Effect`'''

#-------------------------------------------------------------

learnsets_template = '''## `= this.Name` Learnset

**Pokedex Entry:** `= this.Pokedex`

```dataview
TABLE WITHOUT ID
    T[0] AS Learned,
    T[1].Type AS Type,
    T[1] AS Move
FROM #PokeroleSRD/Learnsets
flatten moves as T
where file.path = this.file.path
```
'''

#-------------------------------------------------------------------

natures_template = '''## `= this.Nature`

**Confidence**: `= this.Confidence`

*`= this.Keywords`*

> `= this.Description`
'''

#-------------------------------------------------------------------

items_template = '''## `= this.Name`

*`= this.Description`*

| Type Bonus         | Value          | Heal Amount         | Suggested Price         | PMD Price         |
| ------------------ | -------------- | ------------------- | ----------------------- | ----------------- |
| `= this.TypeBonus` | `= this.Value` | `= this.HealAmount` | `= this.SuggestedPrice` | `= this.PMDPrice` |

**Pokemon Limitation**: `= this.SpecificPokemon`
'''

class SRD(object):
    
    def __init__(self, version="Version20", public_vault=False):
        self.obsidian = secrets['PublicObsidianRoot'] if public_vault else secrets['ObsidianRoot']
        self.path_setup(version)
        self.orphans = None

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
            
        self.pokedex_output = self.obsidian+'/SRD-Pokedex/'
        self.abilities_output = self.obsidian+'/SRD-Abilities/'
        self.moves_output = self.obsidian+'/SRD-Moves/'
        self.learnsets_output = self.obsidian+'/SRD-Learnsets/'
        self.natures_output = self.obsidian+'/SRD-Natures/'
        self.sprites_output = self.obsidian+'/SRD-BoxSprites/'
        self.home_output = self.obsidian+'/SRD-HomeSprites/'
        self.book_output = self.obsidian+'/SRD-BookSprites/'
        self.shuffle_output = self.obsidian+'/SRD-ShuffleTokens/'
        self.items_output = self.obsidian+'/SRD-Items/'

        self.outputs = [self.pokedex_output,self.abilities_output,self.moves_output,
                    self.learnsets_output,self.natures_output,self.sprites_output,
                    self.home_output,self.book_output,self.shuffle_output,self.items_output]

        for p in self.outputs:
            os.makedirs(p,exist_ok=True)
            
        return 0

    def _pokedex(self):
        for src in glob(self.pokedex_path+"/*.json"):
            entry = json.loads(open(src).read())
            name = entry['Name']
            sname = entry['Image'].split('.')
            entry['BoxSprite'] = f"SRD-{sname[0]}-BoxSprite.{sname[1]}"
            entry['HomeSprite'] = f"SRD-{sname[0]}-HomeSprite.{sname[1]}"
            entry['BookSprite'] = f"SRD-{sname[0]}-BookSprite.{sname[1]}"
            entry['ShuffleToken'] = f"SRD-{sname[0]}-ShuffleToken.{sname[1]}"
            
            entry['Legendary'] = 'Yes' if entry['Legendary'] else 'No'
            entry['GoodStarter'] = 'Yes' if entry['GoodStarter'] else 'No'
            entry['Learnset'] = f"[[SRD-{entry['Name']}-Learnset]]"
            
            if entry.get('Evolutions'):
                evocopy = entry['Evolutions'].copy()
                for dat in evocopy:
                    if dat.get('To'):
                        dat['Pokemon'] = f"[[SRD-{dat.get('To')}]]"
                        dat['Evolves'] = 'To'
                        del dat['To']
                    if dat.get('From'):
                        dat['Pokemon'] = f"[[SRD-{dat.get('From')}]]"
                        dat['Evolves'] = 'From'
                        del dat['From']
                evodf = pd.DataFrame(evocopy)
                colorder = ['Evolves', 'Pokemon', 'Kind'] + [x for x in list(evodf.columns) if x not in ['Evolves', 'Pokemon', 'Kind']]
                evodf = evodf.reindex(columns=colorder).fillna('')
                evostring='\n'+evodf.to_markdown(index=0)+'\n'
            else: evostring = ""
            
            abilities = (f"[[SRD-{entry['Ability1']}|{entry['Ability1']}]]"
                                f"{'' if not entry['Ability2'] else ' / [[SRD-'+ entry['Ability2']+'|'+entry['Ability2']+']]'}"
                                f"{'' if not entry['HiddenAbility'] else ' ([[SRD-'+entry['HiddenAbility']+'|'+entry['HiddenAbility']+']])'}"
                                f"{'' if not entry['EventAbilities'] else ' <[[SRD-'+entry['EventAbilities']+'|'+entry['EventAbilities']+']]>'}"
                                )
            INTEGERS = ['BaseHP', 'Strength', 'MaxStrength',
            'Dexterity', 'MaxDexterity', 'Vitality', 'MaxVitality', 'Special',
            'MaxSpecial', 'Insight', 'MaxInsight']
            for key in INTEGERS:
                entry[key] = int(entry[key])

            template =  (
                f"""# `= this.name`\n"""
                f"""\n"""
                f"""> [!grid]\n"""
                f"""> ![[{entry['BookSprite']}|wsmall]]\n"""
                f"""> ![[{entry['HomeSprite']}]]\n"""
                f"""> ![[{entry['BoxSprite']}|htiny]]\n"""
                f"""> ![[{entry['ShuffleToken']}|wsmall]]\n"""
                f"""\n"""
                f"""\n"""
                f"""*{entry['DexCategory']}*\n"""
                f"""*{entry['DexDescription']}*\n"""
                f"""\n"""
                f"""**DexID**:: {entry['DexID']}\n"""
                f"""**Name**:: {name}\n"""
                f"""**Type**:: {entry['Type1']}{f' / {entry["Type2"]}' if entry['Type2'] else ''}\n"""
                f"""**Abilities**:: {abilities}\n"""
                f"""**Base HP**:: {entry['BaseHP']}\n"""
                f"""\n"""
                f"""|           |                                                                                        |                                          |\n"""
                f"""| --------- | -------------------------------------------------------------------------------------- | ---------------------------------------- |\n"""
                f"""| Strength  | `= padleft(padright("",this.MaxStrength - this.Strength,"⭘"),this.MaxStrength,"⬤")`    | (Strength::{entry['Strength']})/(MaxStrength::{entry['MaxStrength']})   |\n"""
                f"""| Dexterity | `= padleft(padright("",this.MaxDexterity - this.Dexterity,"⭘"),this.MaxDexterity,"⬤")` | (Dexterity:: {entry['Dexterity']})/(MaxDexterity::{entry['MaxDexterity']}) |\n"""
                f"""| Vitality  | `= padleft(padright("",this.MaxVitality - this.Vitality,"⭘"),this.MaxVitality,"⬤")`    | (Vitality::{entry['Vitality']})/(MaxVitality::{entry['MaxVitality']})   |\n"""
                f"""| Special   | `= padleft(padright("",this.MaxSpecial - this.Special,"⭘"),this.MaxSpecial,"⬤")`       | (Special::{entry['Special']})/(MaxSpecial::{entry['MaxSpecial']})     |\n"""
                f"""| Insight   | `= padleft(padright("",this.MaxInsight - this.Insight,"⭘"),this.MaxInsight,"⬤")`       | (Insight::{entry['Insight']})/(MaxInsight::{entry['MaxInsight']})     |\n"""
                f"""\n"""
                f"""**Height**: {str(entry['Height']['Feet']).split('.')[0]}'{str(entry['Height']['Feet']).split('.')[1]}" / {entry['Height']['Meters']}m\n"""
                f"""**Weight**: {entry['Weight']['Pounds']}lbs / {entry['Weight']['Kilograms']}kg\n"""
                f"""**Good Starter**:: {entry['GoodStarter']}\n"""
                f"""**Recommended Rank**:: {entry['RecommendedRank']}\n"""
                f"""{evostring}\n"""
                f"""![[SRD-{name}-Learnset]]\n"""
            )
                
            for x in ['DexID','Strength','MaxStrength','Dexterity','MaxDexterity',
                    'Vitality','MaxVitality','Special','MaxSpecial','Insight','MaxInsight',
                    'BaseHP', 'RecommendedRank', 'GoodStarter', '_id', 'Name']:
                del entry[x]
            
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Pokedex\n\n{template}"
            open(self.pokedex_output+f"SRD-{name}.md",'w').write(self.entry_output)
    
    def _abilities(self):
        for src in glob(self.abilities_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Abilities\n\n{ability_template}"
            open(self.abilities_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _moves(self):
        for src in glob(self.moves_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Moves\n\n{moves_template}"
            open(self.moves_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _learnsets(self):
        for src in glob(self.learnsets_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            
            entry['Pokedex'] = f"[[SRD-{entry['Name']}|{entry['Name']}]]"
            moves = []
            for m in entry["Moves"]:
                if moves and m["Learned"] != moves[-1][0]:
                    moves.append(["---------------------------","---------------------------"])
                moves.append([m[f'Learned'],f'[[SRD-{m["Name"]}|{m["Name"]}]]'])
            entry['Moves'] = moves
            entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Learnsets\n\n{learnsets_template}"
            open(self.learnsets_output+f"SRD-{entry['Name']}-Learnset.md",'w').write(entry_output)
    
    def _natures(self):
        for src in glob(self.natures_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Natures\n\n{natures_template}"
            open(self.natures_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _items(self):
        for src in glob(self.items_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Items\n\n{items_template}"
            open(self.items_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
            
    def _images(self):
        def x(path, output, postfix):
            for img in [x for x in os.listdir(path) if '.png' in x]:
                sname = img.split('.')
                srdname = f'SRD-{sname[0]}-{postfix}.{sname[1]}'
                copy(path+img, output+srdname)
                # print(path+img, output+srdname)
        x(self.sprites_path, self.sprites_output, 'BoxSprite')
        x(self.home_path, self.home_output, 'HomeSprite')
        x(self.book_path, self.book_output, 'BookSprite')
        x(self.shuffle_path, self.shuffle_output, 'ShuffleToken')
    
    def _orphan_check(self, start, updates):
        
        targets = {
            "pokedex":   [self.pokedex_output],
            "abilities": [self.abilities_output],
            "moves":     [self.moves_output],
            "learnsets": [self.learnsets_output],
            "natures":   [self.natures_output],
            "items":     [self.items_output],
            "images":    [self.sprites_output,self.home_output,self.book_output]
            }   
        self.orphans = {}
        
        for target in updates:
            for path in targets[target]:
                self.orphans[path] = []
                for f in glob(path+'/*.*'):
                    if os.path.getmtime(f) < start:
                        self.orphans[path].append(f)
        print("INFO: Orphan files (not updated in last update to their folder): ")
        print(json.dumps(self.orphans, indent=4))
        return self.orphans
        
    def _clear_orphans(self, confirm=False):
        if not self.orphans: return 0
        for path in self.orphans.keys():
            for f in self.orphans[path]:
                if not confirm: 
                    conf = input(f'WARN: Delete {f} from SRD Directory? [Y/Yes]: ')
                    if conf.lower() not in ['y', 'yes']:
                        print("INFO: Skipping...")
                    else:
                        print(f'INFO: Deleting {f} from SRD Directory...')
                        os.remove(f)
                else: 
                    print(f'INFO: Deleting {f} from SRD Directory...')
                    os.remove(f)
        
def update(*argv, batch=False, version='Version20', confirm=False, 
        public_vault=False,
        orphans=False, 
        orphan_clear_confirm=False):
        
    srd = SRD(version,public_vault)
    
    if orphans: start = time.time()
    
    targets = {
        "pokedex":   srd._pokedex,
        "abilities": srd._abilities,
        "moves":     srd._moves,
        "learnsets": srd._learnsets,
        "natures":   srd._natures,
        "items":     srd._items,
        "images":    srd._images
    }
    
    updates = list(targets.keys()) if batch else []
    for t in argv:
        if t.lower() in targets:
            updates.append(t.lower())
        else:
            print(f"WARN: Target {t.lower()} not configured, Skipping...")
    updates = set(updates)
    if not confirm: 
        conf = input(f'INFO: {updates}\nQUERY: Update these folders in the SRD? [Y/Yes]: ')
        if conf.lower() not in ['y', 'yes']:
            return "WARN: Did not confirm update, cancelling..."
    else: print(f'INFO: {updates}\nINFO: Updating these folders in the SRD...')
    
    for t in updates:
        func = targets[t]
        func()
        print(f'INFO: Folder {t} updated!')
        
    print('INFO: SRD Update Complete.')
    if orphans: 
        dead = srd._orphan_check(start, updates)
        if str(orphans).lower() == 'clear': srd._clear_orphans(orphan_clear_confirm)
        
def help():
    print("""
    Python Script to update the Obsidian SRD with the latest Data. 
    
    update: 
        update [collection names], [--batch] [--version Version] [--confirm] [--orphans [clear]] [--orphan_clear_confirm]
            collection names     : one or more of the folders in the SRD. Optional when using --batch.
            batch                : Optional. Updates all SRD folderss
            version              : Optional. Changes the Version folder to be used in paths.
            confirm              : Optional. Skips confirmation step. 
            public_vault         : Optional. Changes Obsidian Root pulled from secrets.json
            orphans              : Optional. Runs the Orphan file check. When given "clear" as parameter, 
                                   the script will prompt the user for deletion of Orphans.
            orphan_clear_confirm : Optional. Auto confirms Orphan deletion when using --oprhans clear 
    """)

if __name__ == '__main__':
  fire.Fire()