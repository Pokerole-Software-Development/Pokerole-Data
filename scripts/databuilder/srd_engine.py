from engine import Engine
from fire import Fire
from glob import glob
from os.path import join
from os import listdir
from shutil import copy
import yaml
import pandas as pd

VERBOSE = True

class SRD_Engine(Engine):
    
    def __init__(self, output_path, game_version):
        super().__init__(output_path, game_version)
        self.in_vault_path = join("Pokerole SRD", f"SRD {self.game_version}")
        self.output_path = join(output_path, "Pokerole SRD", f"SRD {self.game_version}")
    
    def pokedex_entry(self, entry):
        # Entry dict is also going to be used for the yml metadata. 
        if VERBOSE: print(entry['Name'])
        name = entry['Name']
        sname = entry['Image'].split('.')
        entry['BookSprite'] = f"SRD-{sname[0]}-BookSprite.{sname[1]}"
        entry['HomeSprite'] = f"SRD-{sname[0]}-HomeSprite.{sname[1]}"
        entry['BoxSprite'] = f"SRD-{sname[0]}-BoxSprite.{sname[1]}"
        entry['ShuffleToken'] = f"SRD-{sname[0]}-ShuffleToken.{sname[1]}"
        
        # entry['Legendary'] = 'Yes' if entry['Legendary'] else 'No'
        # goodstarter = 'Yes' if entry['GoodStarter'] else 'No'
        entry.update(self._learnset_gen(entry['Moves']))
        
        
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
        
        height = str(entry['Height']['Feet'])
        feet = height.split('.')[0]
        inches = height.split('.')[1] if '.' in height else 0 
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
            
        entry_template = open('resources/srd_pokedex_template.txt').read()
        entry_output = entry_template.format( 
            name=name, 
            booksprite=entry['BookSprite'], 
            homesprite=entry['HomeSprite'], 
            boxsprite=entry['BoxSprite'], 
            shuffletoken=entry['ShuffleToken'], 
            dexcategory=entry['DexCategory'], 
            dexdescription=entry['DexDescription'], 
            dexid=entry['DexID'], 
            typeline=entry['Type1']+(f' / {entry["Type2"]}' if entry['Type2'] else ''), 
            abilities=abilities, 
            basehp=entry["BaseHP"], 
            strengthdots = ('⬤'*entry['Strength'])+('⭘'*(entry['MaxStrength']-entry['Strength'])),
            strengthraw = str(entry["Strength"])+'/'+str(entry['MaxStrength']),
            dexteritydots = ('⬤'*entry['Dexterity'])+('⭘'*(entry['MaxDexterity']-entry['Dexterity'])),
            dexterityraw = str(entry["Dexterity"])+'/'+str(entry['MaxDexterity']),
            vitalitydots = ('⬤'*entry['Vitality'])+('⭘'*(entry['MaxVitality']-entry['Vitality'])),
            vitalityraw = str(entry["Vitality"])+'/'+str(entry['MaxVitality']),
            specialdots = ('⬤'*entry['Special'])+('⭘'*(entry['MaxSpecial']-entry['Special'])),
            specialraw = str(entry["Special"])+'/'+str(entry['MaxSpecial']),
            insightdots = ('⬤'*entry['Insight'])+('⭘'*(entry['MaxInsight']-entry['Insight'])),
            insightraw = str(entry["Insight"])+'/'+str(entry['MaxInsight']),
            feet=feet, 
            inches=inches, 
            meters=entry['Height']['Meters'], 
            pounds=entry['Weight']['Pounds'],
            kilograms=entry['Weight']['Kilograms'], 
            goodstarter= 'Yes' if entry['GoodStarter'] else 'No', 
            recommendedrank=entry['RecommendedRank'], 
            evostring=evostring,
            self_in_vault=join(self.in_vault_path, 'SRD-Pokedex', f"SRD-{name}.md")
        )
        
        for x in ['DexID', 'BaseHP', 'RecommendedRank', 'GoodStarter', '_id', 'Name', 'Moves']:
                del entry[x]
        entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Pokedex\n\n{entry_output}"
        
        path = join(self.output_path,'SRD-Pokedex', f"SRD-{name}.md")
        self._write_to(entry_output, path)
        
        return entry_output
    
    def _learnset_gen(self, stored_moves):
        ranks = ['Starter','Beginner','Amateur','Ace','Pro','Rookie','Standard','Advanced','Expert']
        moves = {}
        for k in ranks:
            moves[k+'Moves'] = [m['Name'] for m in stored_moves if m['Learned'] == k]
        return moves
        
    def movedex_entry(self, entry):
        pass
    
    def abilitydex_entry(self, entry):
        ability_template = (
            '''## `= this.name`\n'''
            '''\n'''
            '''> *`= this.Description`*\n'''
            '''\n'''
            '''**Effect:** `= this.Effect`'''
            )
        del entry['_id']
        entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Abilities\n\n{ability_template}"
        path = join(self.output_path,'SRD-Abilities', f"SRD-{entry['Name']}.md")
        self._write_to(entry_output, path)
        
    def itemdex_entry(self, entry):
        
        items_template = (
                f'''## `= this.Name`\n'''
                f'''\n'''
                f'''![[{entry['ItemSprite']}|right]]\n'''
                f'''\n'''
                f'''*`= this.Description`*\n'''
                f'''\n'''
                f'''| Trainer Price           | PMD Price         | Source | \n'''
                f'''| ----------------------- | ----------------- | ------ |\n'''
                f'''| `= this.SuggestedPrice` | `= this.PMDPrice` | `= this.Source`\n'''
                f'''\n'''
                f'''**Pokemon Limitation**: `= this.SpecificPokemon`\n'''
                )
        del entry['_id']
        
        entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Items\n\n{items_template}"
        path = join(self.output_path,'SRD-Items', f"SRD-{entry['Name']}.md")
        self._write_to(entry_output, path)
    
    def nature_entry(self, entry):
        natures_template = (
            '''## `= this.Nature`\n'''
            '''\n'''
            '''**Confidence**: `= this.Confidence`\n'''
            '''\n'''
            '''*`= this.Keywords`*\n'''
            '''\n'''
            '''> `= this.Description`'''
            )
        del entry['_id']
        entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Natures\n\n{natures_template}"
        path = join(self.output_path,'SRD-Natures', f"SRD-{entry['Name']}.md")
        self._write_to(entry_output, path)
    
    def import_images(self, source, setname):
        target_path = join(self.output_path, f'SRD-{setname}')
        self._pathgen(target_path)
        self._copy_imageset(source, target_path, '', f'-{setname[:-1]}')