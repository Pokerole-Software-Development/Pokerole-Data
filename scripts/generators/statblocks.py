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

class Statblocks(object):
    
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

        self.outputs = [self.pokedex_output,self.abilities_output,self.moves_output,
                    self.natures_output,self.sprites_output,self.home_output,
                    self.book_output,self.shuffle_output,self.items_output]

        for p in self.outputs:
            os.makedirs(p,exist_ok=True)
            
        return 0

    def _pokedex(self):
        for src in glob(self.pokedex_path+"/*.json"):
            entry = json.loads(open(src).read())
            types = f"""{entry['Type1']}{f' / {entry["Type2"]}' if entry['Type2'] else ''}"""
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
                entry = json.loads(open(self.moves_path+f'/{m["Name"]}.json').read())
                damage = '' if entry['Category'] == "Support" else f"""with a damage pool of *{entry['Damage1']}+{entry['Power']}*"""
                effect = '' if entry['Effect'] == '-' else f""" **Effect:** {entry['Effect']}"""
                x = f'''- [ ] **{entry['Name']}** - *{entry['Type']} Type* {entry['Category']} Move learned at *{m['Learned']}*. Targets *{entry['Target']}*. It's Accuracy dice are *{entry["Accuracy1"]}+{entry["Accuracy2"]}*{damage}.{effect}\n'''
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
            print(''.join(template))
            break
            # self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Pokedex\n\n{template}"
            # open(self.pokedex_output+f"SRD-{name}.md",'w').write(self.entry_output)
    
    def _learnset_gen(self, stored_moves):
            moves = []
            for m in stored_moves:
                entry = json.loads(open(self.moves_path+f'/{m["Name"]}.json').read())
                damage = '' if entry['Category'] == "Support" else f"""with a damage pool of *{entry['Damage1']}+{entry['Power']}*"""
                effect = '' if entry['Effect'] == '-' else f""" **Effect:** {entry['Effect']}"""
                x = f'''- [ ] **{entry['Name']}** - *{entry['Type']} Type* {entry['Category']} Move learned at *{m['Learned']}*. Targets *{entry['Target']}*. It's Accuracy dice are *{entry["Accuracy1"]}+{entry["Accuracy2"]}*{damage}.{effect}\n'''
                moves.append(x)
            return moves
        
def update(*argv, batch=False, version='Version20', confirm=False, 
        public_vault=False,
        orphans=False, 
        orphan_clear_confirm=False):
        
    srd = Statblocks(version,public_vault)
    
    if orphans: start = time.time()
    
    targets = {
        "pokedex":   srd._pokedex
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