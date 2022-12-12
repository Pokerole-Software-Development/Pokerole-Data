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
            open(self.pokedex_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _abilities(self):
        for src in glob(self.abilities_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            open(self.abilities_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _moves(self):
        for src in glob(self.moves_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            open(self.moves_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _learnsets(self):
        for src in glob(self.learnsets_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            
            entry['Species'] = f"[[SRD-{entry['Name']}|{entry['Name']}]]"
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
            open(self.natures_output+f"SRD-{entry['Name']}.md",'w').write(self.entry_output)
    
    def _items(self):
        for src in glob(self.items_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
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
        
def update(*argv, batch=False, version='Version20', confirm=False):
        
    srd = SRD(version)
    
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
    else: print(f'INFO: {updates}\nQUERY: Updating these folders in the SRD...')
    
    for t in updates:
        func = targets[t]
        func()
        print(f'INFO: Folder {t} updated!')
        
    print('INFO: Foundry Update Complete.')
        
def help():
    print("""
    Python Script to update the Obsidian SRD with the latest Data. 
    
    update: 
        update [collection names], [--batch] [--version Version] [--confirm] [--orphans [clear]] [--orphan_clear_confirm]
            collection names     : one or more of the folders in the SRD. Optional when using --batch.
            batch                : Optional. Updates all SRD folderss
            version              : Optional. Changes the Version folder to be used in paths.
            confirm              : Optional. Skips confirmation step. 
    """)

if __name__ == '__main__':
  fire.Fire()