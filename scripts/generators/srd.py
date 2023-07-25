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

| Type          | Target          | Category          | Power          |
| ------------- | --------------- | ----------------  | -------------- |
| `= this.Type` | `= this.Target` | `= this.Category` | `= this.Power` | 

**Effect:** `= this.Effect`'''

#-------------------------------------------------------------------

natures_template = '''## `= this.Nature`

**Confidence**: `= this.Confidence`

*`= this.Keywords`*

> `= this.Description`
'''

#-------------------------------------------------------------------

items_template = '''## `= this.Name`

*`= this.Description`*

| Trainer Price           | PMD Price         | Source | 
| ----------------------- | ----------------- | ------ |
| `= this.SuggestedPrice` | `= this.PMDPrice` | `= this.Source` 

**Pokemon Limitation**: `= this.SpecificPokemon`
'''

class SRD(object):
    
    def __init__(self, version="Version20", public_vault=False):
        self.obsidian = secrets['PublicObsidianRoot'] if public_vault else secrets['ObsidianRoot']
        self.obsidian_relroot = secrets['PublicObsidianRelRoot'] if public_vault else secrets['ObsidianRelRoot']
        self.path_setup(version)
        self.orphans = None

    def path_setup(self, version):
        
        self.pokedex_path = f'../../{version}/Pokedex'
        self.abilities_path = f'../../{version}/Abilities'
        self.moves_path = f'../../{version}/Moves'
        self.natures_path = f'../../{version}/Natures'
        self.sprites_path = '../../Images/BoxSprites/'
        self.home_path = '../../Images/HomeSprites/'
        self.book_path = '../../Images/BookSprites/'
        self.shuffle_path = '../../Images/ShuffleTokens/'
        self.items_path = f'../../{version}/Items/'

        paths = [self.pokedex_path,self.abilities_path,self.moves_path
                 ,self.natures_path,self.sprites_path,self.home_path,
                 self.book_path,self.shuffle_path,self.items_path]
        
        for p in paths:
            if not os.path.exists(p): raise Exception(f"ERROR: Path {p} not found!")
            
        self.pokedex_output = self.obsidian+'/SRD-Pokedex/'
        self.pokedex_rel_output = self.obsidian_relroot+'/SRD-Pokedex/'
        self.abilities_output = self.obsidian+'/SRD-Abilities/'
        self.moves_output = self.obsidian+'/SRD-Moves/'
        self.natures_output = self.obsidian+'/SRD-Natures/'
        self.sprites_output = self.obsidian+'/SRD-BoxSprites/'
        self.home_output = self.obsidian+'/SRD-HomeSprites/'
        self.book_output = self.obsidian+'/SRD-BookSprites/'
        self.shuffle_output = self.obsidian+'/SRD-ShuffleTokens/'
        self.items_output = self.obsidian+'/SRD-Items/'
        self.statblock_output = self.obsidian+'/SRD-Statblocks/'

        self.outputs = [self.pokedex_output,self.abilities_output,self.moves_output,
                    self.natures_output,self.sprites_output,self.home_output,
                    self.book_output,self.shuffle_output,self.items_output]

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
            entry['Moves'] = self._learnset_gen(entry['Moves'])
            
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
                f"""## Learnset\n\n"""
                f"""```dataview\n"""
                f"""TABLE WITHOUT ID\n"""
                f"""    T[0] AS Learned,\n"""
                f"""    T[1].Type AS Type,\n"""
                f"""    T[1] AS Move\n"""
                f"""FROM "{self.pokedex_rel_output+f"SRD-{name}.md"}"\n"""
                f"""flatten moves as T\n"""
                f"""where file.path = this.file.path\n"""
                f"""```\n"""
            )
                
            for x in ['DexID','Strength','MaxStrength','Dexterity','MaxDexterity',
                    'Vitality','MaxVitality','Special','MaxSpecial','Insight','MaxInsight',
                    'BaseHP', 'RecommendedRank', 'GoodStarter', '_id', 'Name']:
                del entry[x]
            
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Pokedex\n\n{template}"
            open(self.pokedex_output+f"SRD-{name}.md",'w').write(self.entry_output)
    
    def _learnset_gen(self, stored_moves):
            moves = []
            for m in stored_moves:
                if moves and m["Learned"] != moves[-1][0]:
                    moves.append(["---------------------------","---------------------------"])
                moves.append([m[f'Learned'],f'[[SRD-{m["Name"]}|{m["Name"]}]]'])
            return moves
        
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
    
    def _statblocks(self):
        for src in glob(self.pokedex_path+"/*.json"):
            entry = json.loads(open(src).read())

            types = f"""{entry['Type1']}{f'/{entry["Type2"]}' if entry['Type2'] else ''}"""
            abilities = ''
            for ability in [entry['Ability1'], entry['Ability2'], entry['HiddenAbility'], entry['EventAbilities']]:
                if ability: 
                    abentry = json.loads(open(self.abilities_path+f'/{ability}.json').read())
                    abilities+=(f"- **{abentry['Name']}** {abentry['Effect']}\n")
            HitP = entry['Vitality']+entry['BaseHP']
            Init = entry['Dexterity']
            PClash = entry['Strength']
            SClash = entry['Special']
            Strength = f"{entry['Strength']}/{entry['MaxStrength']}"
            Dexterity = f"{entry['Dexterity']}/{entry['MaxDexterity']}"
            Vitality = f"{entry['Vitality']}/{entry['MaxVitality']}"
            Special = f"{entry['Special']}/{entry['MaxSpecial']}"
            Insight = f"{entry['Insight']}/{entry['MaxInsight']}"

            moves = []
            for m in entry['Moves']:
                try:
                    mentry = json.loads(open(self.moves_path+f'/{m["Name"]}.json').read())
                except FileNotFoundError:
                    pass
                damage = '' if mentry['Category'] == "Support" else f""" with a damage pool of *{mentry['Damage1']}+{mentry['Power']}*"""
                effect = '' if mentry['Effect'] == '-' else f""" **Effect:** {mentry['Effect']}"""
                # effect = '' if mentry['Effect'] == '-' else f"""\n    - **Effect:** {mentry['Effect']}"""
                x = f'''- [ ] **{mentry['Name']}** - *{mentry['Type']} Type* {mentry['Category']} Move learned at *{m['Learned']}*. Targets *{mentry['Target']}*. It's Accuracy dice are *{mentry["Accuracy1"]}+{mentry["Accuracy2"]}*{damage}.{effect}\n\n'''
                moves.append(x)

            template =  (
                f"#### {entry['Name']}\n",
                f"\n",
                f"A **{types}** Pokemon with a **Nature** nature at **Rank** rank. It's **Abilities** are:\n",
                f"\n",
                f"{abilities}\n",
                f"\n",
                f"##### Stats\n",
                f"\n",
                f"| **HP ({entry['BaseHP']})**  | **Init**  | **Evade** | **Phys Clash** | **Spec Clash** |\n",
                f"| -------- | --------- | --------- | -------------- | -------------- |\n",
                f"| {HitP}   | {Init}    | {Init}    | {PClash}      | {SClash}     |\n",
                f"| **Str**   | **Dex**  | **Vit**    | **Spec**   | **Ins**  |\n",
                f"| {Strength}| {Dexterity} | {Vitality}| {Special}| {Insight}|\n",
                f"| **Tough** | **Cool** | **Beauty** | **Clever** | **Cute** |\n",
                f"| 1         | 1        | 1          | 1          | 1        |\n",
                f"\n",
                f"##### Skills\n",
                f"\n",
                f"| Skill | Skill | Skill | Skill | Skill | Skill | Skill | Skill |\n",
                f"| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |\n",
                f"|       |       |       |       |       |       |       |       |\n",
                f"\n",
                f"\n",
                f"##### Moves\n"
                f"\n",
                f"{''.join(moves)}"
                )

            self.entry_output = f"#PokeroleSRD/Statblock\n\n{''.join(template)}"
            open(self.statblock_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _orphan_check(self, start, updates):
        
        targets = {
            "pokedex":   [self.pokedex_output],
            "abilities": [self.abilities_output],
            "moves":     [self.moves_output],
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
        "pokedex":    srd._pokedex,
        "abilities":  srd._abilities,
        "moves":      srd._moves,
        "natures":    srd._natures,
        "items":      srd._items,
        "images":     srd._images,
        "statblocks": srd._statblocks
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