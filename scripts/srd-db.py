from DataBuilder import DataBuilder
from fire import Fire
from glob import glob
from os.path import join
from os import listdir
from shutil import copy
import json
import yaml
import pandas as pd

class SRD_DataBuilder(DataBuilder):
    
    def __init__(self, 
                root='../',
                version='v2.1',
                obsidian='/Users/bill/Code/Pokerole SRD'
                # obsidian='/Users/bill/Library/Mobile Documents/iCloud~md~obsidian/Documents/Writers Room'
                ):
        super().__init__(root, version)
        self.obsidian = join(obsidian, "Pokerole SRD", f"SRD {self.version}")
        self.in_vault_path = join("Pokerole SRD", f"SRD {self.version}")
        
    def _srd_path_prep(self, source, output):
        path = self._pathgen(source)
        outpath = self._pathgen(output, root=self.obsidian, does_exist=False)
        return path, outpath
        
    def build_pokedex(self, source="{version}/Pokedex", output='SRD-Pokedex'):
        pokedex_path, pokedex_output = self._srd_path_prep(source, output)
        for src in glob(pokedex_path+"/*.json"):
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
                f"""**Height**: {feet}'{inches}" / {entry['Height']['Meters']}m\n"""
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
                # f"""FROM "{f""}"\n"""
                # f"""FROM "{join(self.in_vault_path, f"SRD-{name}.md")}"\n"""
                f"""FROM "{join(self.in_vault_path, output, f"SRD-{name}.md")}"\n"""
                f"""flatten moves as T\n"""
                f"""where file.path = this.file.path\n"""
                f"""```\n"""
            )
                
            for x in ['DexID','Strength','MaxStrength','Dexterity','MaxDexterity',
                    'Vitality','MaxVitality','Special','MaxSpecial','Insight','MaxInsight',
                    'BaseHP', 'RecommendedRank', 'GoodStarter', '_id', 'Name']:
                del entry[x]
            
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Pokedex\n\n{template}"
            open(join(pokedex_output, f"SRD-{name}.md"),'w').write(self.entry_output)

    def _learnset_gen(self, stored_moves):
        moves = []
        for m in stored_moves:
            if moves and m["Learned"] != moves[-1][0]:
                moves.append(["---------------------------","---------------------------"])
            # moves.append([m[f'Learned'],f'[[SRD-{m["Name"]}|{m["Name"]}]]'])
            moves.append([m[f'Learned'], f'''[[{join(self.in_vault_path, 'SRD-Moves', 'SRD-'+m["Name"])}|{m["Name"]}]]'''])
        return moves

    def build_abilities(self, source="{version}/Abilities", output='SRD-Abilities'):
        abilities_path, abilities_output = self._srd_path_prep(source, output)
        ability_template = (
            '''## `= this.name`\n'''
            '''\n'''
            '''> *`= this.Description`*\n'''
            '''\n'''
            '''**Effect:** `= this.Effect`'''
            )

        for src in glob(abilities_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Abilities\n\n{ability_template}"
            open(join(abilities_output,f"SRD-{entry['Name']}.md"),'w').write(self.entry_output)
    
    def build_moves(self, source="{version}/Moves", output='SRD-Moves'):
        moves_path, moves_output = self._srd_path_prep(source, output)
        moves_template = (
        '''### `= this.name`\n'''
        '''*`= this.Description`*\n'''
        '''\n'''
        '''**Accuracy:** `= this.Accuracy1` + `= this.Accuracy2`\n'''
        '''**Damage:** `= this.Power` `= choice(length(this.Damage1)=0, "","\+ "+ this.Damage1)` `= choice(length(this.Damage2)=0, "","\+ "+ this.Damage2)`\n'''
        '''\n'''
        '''| Type          | Target          | Category          | Power          |\n'''
        '''| ------------- | --------------- | ----------------  | -------------- |\n'''
        '''| `= this.Type` | `= this.Target` | `= this.Category` | `= this.Power` | \n'''
        '''\n'''
        '''**Effect:** `= this.Effect`'''
        )
        
        for src in glob(moves_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Moves\n\n{moves_template}"
            open(join(moves_output, f"SRD-{entry['Name']}.md"),'w').write(self.entry_output)
    
    def build_natures(self, source="{version}/Natures", output='SRD-Natures'):
        natures_path, natures_output = self._srd_path_prep(source, output)
        natures_template = (
            '''## `= this.Nature`\n'''
            '''\n'''
            '''**Confidence**: `= this.Confidence`\n'''
            '''\n'''
            '''*`= this.Keywords`*\n'''
            '''\n'''
            '''> `= this.Description`'''
            )
        
        for src in glob(natures_path+"/*.json"):
            entry = json.loads(open(src).read())
            del entry['_id']
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Natures\n\n{natures_template}"
            open(join(natures_output,f"SRD-{entry['Name']}.md"),'w').write(self.entry_output)
    
    def build_items(self, source="{version}/Items", output='SRD-Items'):
        items_path, items_output = self._srd_path_prep(source, output)
        for src in glob(items_path+"/*.json"):
            entry = json.loads(open(src).read())
            # TODO: add an Image key to items so it doesn't need a default .png
            entry['ItemSprite'] = f"SRD-{entry['_id']}-ItemSprite.png"
            
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
            self.entry_output = f"---\n{yaml.dump(entry)}---\n\n#PokeroleSRD/Items\n\n{items_template}"
            open(join(items_output, f"SRD-{entry['Name']}.md"),'w').write(self.entry_output)
            
    def _copy_imageset(self, source, output, postfix):
        for img in [x for x in listdir(source) if '.png' in x]:
            sname = img.split('.')
            srdname = f'SRD-{sname[0]}-{postfix}.{sname[1]}'
            copy(join(source, img), join(output, srdname))
            # print(join(source, img), join(output, srdname))

    def build_boxsprites(self, source="Images/BoxSprites", output='SRD-BoxSprites'):
        inpath, outpath = self._srd_path_prep(source, output)
        self._copy_imageset(inpath, outpath, 'BoxSprite')
        
    def build_homesprites(self, source="Images/HomeSprites", output='SRD-HomeSprites'):
        inpath, outpath = self._srd_path_prep(source, output)
        self._copy_imageset(inpath, outpath, 'HomeSprite')

    def build_booksprites(self, source="Images/BookSprites", output='SRD-BookSprites'):
        inpath, outpath = self._srd_path_prep(source, output)
        self._copy_imageset(inpath, outpath, 'BookSprite')

    def build_shuffletokens(self, source="Images/ShuffleTokens", output='SRD-ShuffleTokens'):
        inpath, outpath = self._srd_path_prep(source, output)
        self._copy_imageset(inpath, outpath, 'ShuffleToken')

    def build_itemsprites(self, source="Images/ItemSprites", output='SRD-ItemSprites'):
        inpath, outpath = self._srd_path_prep(source, output)
        self._copy_imageset(inpath, outpath, 'ItemSprite')
    
    def build_images(self, source="", output=''):
        self.build_booksprites()
        self.build_boxsprites()
        self.build_homesprites()
        self.build_itemsprites()
        self.build_shuffletokens()
    
    def build_statblocks(self, source="{version}/Pokedex", output='SRD-Statblocks'):
        return 0
        pokedex_path, pokedex_output = self._srd_path_prep(source, output)
        for src in glob(pokedex_path+"/*.json"):
            entry = json.loads(open(src).read())

            types = f"""{entry['Type1']}{f'/{entry["Type2"]}' if entry['Type2'] else ''}"""
            abilities = ''
            for ability in [entry['Ability1'], entry['Ability2'], entry['HiddenAbility'], entry['EventAbilities']]:
                if ability: 
                    abentry = json.loads(open(abilities_path+f'/{ability}.json').read())
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
    
if __name__ == '__main__':
    # The SRD is created in Pokerole SRD/SRD {Version} under the obsidian folder.
    Fire(SRD_DataBuilder)