from glob import glob
import json
from pymongo import MongoClient
import os
import fire

secrets = json.load(open('../../secrets.json'))
client = MongoClient(host='aurii.us', port=20180, username=secrets['MongoUser'], password=secrets['MongoPass'])

def _publish(dataset, path='', fname_key='', chunk_size=0, mongo=None):
    if mongo is not None: mongo.delete_many({})
    if chunk_size:
        chunks = []
        for i in range(0,len(dataset),chunk_size):
            chunks.append(dataset[i:i+chunk_size])
    else: chunks = dataset
    
    for i in range(len(chunks)):
        if path: 
            fname = chunks[i][fname_key] if fname_key else f"{os.path.basename(path)}{i}"
            open(path+f"/{fname}.json",'w').write(json.dumps(chunks[i], indent=4))
        if mongo is not None: 
            if type(chunks[i]) == list: mongo.insert_many(chunks[i])
            else: mongo.insert_one(chunks[i])

def update(*argv, batch=False, version='Version20', confirm=False):
    db = client['Pokerole20']
    
    targets = {
        "pokedex":   [f'../../{version}/Pokedex', db.Pokedex],
        "abilities": [f'../../{version}/Abilities', db.Abilities],
        "moves":     [f'../../{version}/Moves', db.Moves],
        "learnsets": [f'../../{version}/Learnsets', db.Learnsets],
        "natures":   [f'../../{version}/Natures', db.Natures],
        "items":     [f'../../{version}/Items', db.Items]
    }
    for t in targets: 
        if not os.path.exists(targets[t][0]): 
            return f"ERROR: '{targets[t][0]}' collection path not found."
    print(f"INFO: Updating using {version}...")
    
    updates = list(targets.keys()) if batch else []
    for t in argv:
        if t.lower() in targets:
            updates.append(t.lower())
        else:
            print(f"WARN: Target {t.lower()} not configured, Skipping...")
    updates = set(updates)
    if not confirm: 
        conf = input(f'INFO: {updates}\nQUERY: Update these database collections? [Y/Yes]: ')
        if conf.lower() not in ['y', 'yes']:
            return "WARN: Did not confirm update, cancelling..."
    else: print(f'INFO: {updates}\nQUERY: Updating these database collections...')
    
    for t in updates:
        path, collec = targets[t]
        data = []
        for src in sorted(glob(path+"/*.json")):
            data.append(json.loads(open(src).read()))
        _publish(data, fname_key="Name", mongo=collec)
        print(f'INFO: Collection {t} updated!')
    
def help():
    print("""
    Python Script to update the Mongo DB version of the data.
    
    update: 
        update [collection names], [--batch] [--version Version] [--confirm]
            collection names : one or more of the database collections. Optional when using --batch.
            batch            : Optional. Updates all known collections
            version          : Optional. Changes the Version folder to be used in paths.
            confirm          : Optional. Skips confirmation step. 
    """)

if __name__ == '__main__':
  fire.Fire()