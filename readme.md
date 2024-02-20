# Pokerole Dataset

This repo is a Source of Truth for the [Pokerole](https://www.pokeroleproject.com/) tabletop game. This is a developer focused repository: if you're not a programmer, you probably want to check the list of applications built off of this data. 

- This repo contains JSON documents for Pokemon, Natures, Abilities, Moves, and Learnsets for the Pokerole system. 
- It will preserve 2.0 data alongside 2.1 data when 2.1 is released. 
- The repo has a sprite library with filenames consistent with the JSON data.

# Applications Using The Dataset

- [Pokerole Obsidian SRD](https://github.com/Willowlark/PokeroleObsidianSRD) A SRD of the entire Pokerole dataset available within [Obsidian](https://obsidian.md/), a markdown note application. 
- [Pokerole Foundry Module](https://github.com/tech-ticks/foundry-pokerole) A module for the [Foundry VTT system](https://foundryvtt.com/) using the data compiled here.
- [Pokerole Buddy](https://discord.com/channels/245675629515767809/641511676251865118/1208309716548198451) A standalone character sheet application with dozens of useful features

## Developer Information

## A quick tour of the Repository

- **Images** image data that can be referenced from the data. Pokemon currently have a "Sprite" attribute contains the filename of that Pokemon's image. 
  - There are three subfolders to pull from, depending on your needs, HomeSprites for Pokemon Home, BoxSprites for BoxSprites, and BookSprites for the Pokerole core book images.
  - There is a sprite field in each JSON that corresponds to the name of the file in each folder for that pokemon. You can get any of those sprites by using the appropriate base url and that filename. 
  - Book Sprites Base Url: `https://raw.githubusercontent.com/Willowlark/Pokerole-Data/master/images/BookSprites/`
  - Box Sprites Base Url: `https://raw.githubusercontent.com/Willowlark/Pokerole-Data/master/images/BoxSprites/`
  - Home Sprites Base Url: `https://raw.githubusercontent.com/Willowlark/Pokerole-Data/master/images/HomeSprites/`
  - Home Sprites Base Url: `https://raw.githubusercontent.com/Willowlark/Pokerole-Data/master/images/ShuffleTokens/`
- **Raw** data used in the generation of the proper datasets. It is NOT recommended to use data in here for any application, as it has not been processed. It's mostly here for record keeping purposes.
- **Scripts** a folder for any code that manipulates data. At the moment, there should be NO REASON to try and run these, they are for maintainence only.
- **Version20** contains the entire JSON dataset for Pokerole Version 2.0. Each item in the dataset has it's own JSON document. *All of this data is also accessable via Mongo, see below.*
- **DDL.md** contains tables documenting the data in the JSON documents for reference.

## Assisting the Project

This project's home is the `tool-developing` channel on the [Pokerole Discord](https://discord.gg/95DFpdMVcC). If you'd like to develop a project based off this data, or would like to help expand and error check the dataset, reach out there. There's lots to do! 

Check the enhancement issues for anything we've identified that's need doing as well, can always use more help!

# Credits and Contacts

- Needless to say, Pokemon is owned by Nintendo
- I can be contacted through Github (here) or Discord where my username is Willowlark#2359 as the primary maintainer. 
- The original data (`raw/PokeroleBot`) that was used to generate the base dataset was compiled out of the book by Shadeslayer into this [repository](https://github.com/XShadeSlayerXx/PokeRole-Discord.py-Base). 
- `raw/XMLDump` was dumped by SirIntellegence(Brain-Storm.exe) and is sourced from [this repository](https://github.com/SirIntellegence/pokerole-tools/releases/tag/v0.0.0)
- Box sprites were compiled from this [repository](https://github.com/msikma/pokesprite).
- Home sprites were ripped from [the spriter's resource](https://www.spriters-resource.com/nintendo_switch/pokemonhome/).
- [Pokerole](https://www.pokeroleproject.com/) was written by it's own team, check them out. They provided the Booksprites as well.
- Pokemon Shuffle style tokens were provided by Shaedn on this Discord
