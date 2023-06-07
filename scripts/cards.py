import json
import os
import re
import pandas as pd
from shutil import copy, move
import copy 
import io 
import fire

moves_path = '../Version20/Moves/'

def create_json():

    template = {
        "count": "1",
        "color": "dimgray",
        "title": "Headbutt",
        "icon": "white-book-1",
        "icon_back": "",
        "contents": [
        "subtitle | Power {}: {}",
        "property | Type | Normal",
        "property | Accuracy | Dexterity + Brawl",
        "property | Damage | Strength + 3",
        "property | Added Effect | Roll 3 Chance Dice to Flinch. May call Random Encounters when hitting trees.",
        "rule",
        "text | The user strikes the foe with its hard head. Perfect for taking down fruits from trees or shake Pokémon out of their nests on treetops."
        ],
        "tags": [],
        "title_size": "14",
        "card_font_size": "12"
    }

    meta = pd.read_csv(io.StringIO(
"""Type,Color,Icon
Bug,olive,gold-scarab
Dark,black,moon
Dragon,mediumslateblue,spiked-dragon-head
Electric,gold,electric
Fairy,pink,sparkles
Fighting,firebrick,boxing-glove
Fire,darkorange,fire
Flying,mediumorchid,fluffy-wing
Ghost,mediumpurple,spectre
Grass,limegreen,new-shoot
Ground,goldenrod,earth-spit
Ice,paleturquoise,frozen-orb
Normal,dimgrey,moon-orbit
Poison,indigo,death-skull
Psychic,orchid,flower-twirl
Rock,saddlebrown,rock
Steel,silver,big-gear
Water,royalblue,big-wave"""),sep=',').set_index("Type")

    cards = []
    for fname in sorted(os.listdir(moves_path)):
        if '.json' not in fname: continue
        path = moves_path+fname
        data = json.loads(open(path).read())
        card = copy.deepcopy(template)
        card['title'] = data['Name']
        if data['Type'] in meta.index:
            card['color'] = meta.loc[data["Type"], 'Color']
            card['icon'] = meta.loc[data["Type"], 'Icon']
        card['contents'] = [
            f"subtitle | Power {data['Power']}: {data['Category']}",
            f"property | Type | {data['Type']}",
            f"property | Accuracy | {data['Accuracy1']} + {data['Accuracy2']}",
            f"property | Damage | {data['Damage1']} + {data['Power']}",
            f"property | Added Effect | {data['Effect']}",
            f"rule",
            f"text | {data['Description']}"
        ]
        cards.append(card)

    open('../Version20/move_cards.json','w').write(json.dumps(cards, indent=4))

def name_fix():
    for name, card in zip(
            sorted([x for x in os.listdir(moves_path) if '.json' in x]),
            sorted([x for x in os.listdir('../Version20/Move Cards') if '.png' in x])):
        
        move(f'../Version20/Move Cards/{card}',
             f"../Version20/Move Cards/{name.split('.')[0]}.png")
        
if __name__ == '__main__':
  fire.Fire()