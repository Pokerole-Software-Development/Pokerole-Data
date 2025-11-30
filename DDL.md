# JSON DDL 

## Dex Ids

DexID matches the following pattern `\d{4}([GAHPXY]|F\d)` which in simple terms is the four digit pokedex number plus an indicator of variant. DexID is used in the Pokedex and Learnset data structures. 

- **Variants**: 
    - **G**alar, 
    - **A**lolan, 
    - **H**isuian, 
    - **P**aldean, 
    - **X** Mega, 
    - **Y** Mega Variant, 
    - **F#** Form (with Number to id multiple forms)

## Pokedex

Any field that has "Yes" in the Null column can be left blank, and will be for a number of Pokemon. 

| Field           | Data Type | Null? | Notes                                                                |
| --------------- | --------- | ----- | -------------------------------------------------------------------- |
| Number          | int       |       | Pokedex Number of this Species                                       |
| DexID           | String    |       | Pokedex Number + variant flags, if any                               |
| Name            | String    |       | Pokemon Species name                                                 |
| Type1           | String    |       | Type                                                                 |
| Type2           | String    | Yes   | Name of Type                                                         |
| BaseHP          | int       |       | Base HP value                                                        |
| Strength        | int       |       | Base Strength score for the Species                                  |
| MaxStrength     | int       |       | Max Strength score for the Species                                   |
| Dexterity       | int       |       | Base Dexterity score for the Species                                 |
| MaxDexterity    | int       |       | Max Dexterity score for the Species                                  |
| Vitality        | int       |       | Base Vitality score for the Species                                  |
| MaxVitality     | int       |       | Max Vitality score for the Species                                   |
| Special         | int       |       | Base Special score for the Species                                   |
| MaxSpecial      | int       |       | Max Special score for the Species                                    |
| Insight         | int       |       | Base Insight score for the Species                                   |
| MaxInsight      | int       |       | Max Insight score for the Species                                    |
| Ability1        | String    |       | Ability Name                                                         |
| Ability2        | String    | Yes   | Ability Name                                                         |
| HiddenAbility   | String    | Yes   | Ability Name. If this isn't already filled in, you can ignore it.    |
| EventAbilities  | String    | Yes   | Ability Name. If this isn't already filled in, you can ignore it.    |
| RecommendedRank | String    |       | Rank the Species MIGHT be found in the wild                          |
| GenderType      | String    | Yes   | Empty String unless Species has unique gender forms, then "M" or "F" |
| Legendary       | Bool      |       | Flag for Legendaries (Specifically, with max stats by default)       |
| GoodStarter     | Bool      |       | Flag to be set if the good starter symbol is on the Pokedex entry    |
| \_id            | String    |       | Name field, but spaces replaced with '-' and all lowercase           |
| DexCategory     | String    |       | "So and So Pokemon" label from Pokedex                               |
| Height          | Object    |       | Height in Feet and Meters. Both Floats/decimals.                     |
| Weight          | Object    |       | Weight in Kilograms and Pounds. Both Floats/decimals.                |
| DexDescription  | String    |       | Pokedex flavor text                                                  |
| Evolutions      | List      |       | List of Objects. See Evolution objects below                         |
| Image           | String    |       | Basename for this pokemon's sprites                                  |
| Moves           | List      |       | List of Objects. See Learnset below.                                 |

### Evolution Objects

It's possible to have no Evolution objects in the list. 

Anything with "Remove" in the Null? column means you remove that entry entirely when the Pokemon doesn't have that information. 

| Field   | Data Type | Null? | Notes                                                                            |
| ------- | --------- | ----- | -------------------------------------------------------------------------------- |
| To      | String    |       | The name of a Pokemon this Pokemon evolves into. From/To are mutually exclusive. |
| From    | String    |       | The name of a Pokemon this Pokemon evolves from. From/To are mutually exclusive. |
| Kind    | String    |       | How the Pokemon evolves. (Mega, Level, Stone, etc...)        |
| Speed   | String    |Remove | Evolution Speed of a Level based evolution. Only present when kind is Level      |
| Item    | String    |Remove | Evolution item required for evolution. Only present when kind is requires Item.  |
| Stat    | String    |Remove | Stat to check for evolution for Stat based evolution                             |
| Value   | String    |Remove | Stat value to check for evolution via stat based evolution                       |
| Special | String    |Remove | Other note for evolutions                                                       | 

```json
"Evolutions": [
        {
            "From": "Sprigatito",
            "Kind": "Level",
            "Speed": "Medium"
        },
        {
            "To": "Meowscarada",
            "Kind": "Level",
            "Speed": "Medium"
        }
    ]
```

### Learnset Objects

| Field   | Data Type | Null? | Notes                       |
| ------- | --------- | ----- | --------------------------- |
| Learned | String    |       | Rank the move is learned at |
| Name    | String    |       | The name of the Move        | 

```json
 "Moves": [
        {
           "Learned": "Starter",
           "Name": "Scratch"
        },
        {
           "Learned": "Starter",
           "Name": "Tail Whip"
        }
        ... And so on
]
```

## Moves

| Field        | Type   | Null? | Notes                                                                  |
| ------------ | ------ | ----- | ---------------------------------------------------------------------- |
| Name         | String |       | Name of the Move                                                       |
| Type         | String |       | Type of the Move                                                       |
| Power        | int    |       | Power value of the move                                                |
| Damage1      | String |Yes    | Attribute Name or Empty String                                         |
| Damage2      | String |Yes    | Second Damage Pool source or Empty String                              |
| Accuracy1    | String |       | Attribute Name                                                         |
| Accuracy2    | String |       | Skill Name                                                             |
| Target       | String |       | What is targeted by Move. See pg.68 in 3.0                             |
| Effect       | String |       | Move's effect text                                                     |
| Description  | String |       | Description text for move                                              |
| \_id         | String |       | Same as Name, unique for the system. Lowercase and - instead of space. | 
| Attributes   | Object |       | Values that are used by Foundry, to be entered by Foundry team.        |
| AddedEffects | Object |       | Values that are used by Foundry, to be entered by Foundry team.        |
| Category     | String |       | Physical, Special, Support                                             |

## Abilities

| Field       | Type   | Notes                                                                  |
| ----------- | ------ | ---------------------------------------------------------------------- |
| \_id        | String | Same as Name, unique for the system. Lowercase and - instead of space. | 
| Name        | String | Name of Ability                                                        |
| Effect      | String | Effect text of Ability                                                 |
| Description | String | Flavor Text description of Ability                                     |


## Natures

| Field       | Type   | Notes                                             |
| ----------- | ------ | ------------------------------------------------- |
| \_id        | String | Same as Name, unique for the syste. Lowercase and - instead of space.              |
| Name        | String | Name of Nature                                    |
| Nature      | String | Name and Confidence in format "Name (confidence)" |
| Confidence  | int    | Confidence score of the Nature                    |
| Description | String | Text Description of Nature                        |
| Keywords    | String | Comma separated keywords for the Nature           |

## Items

| Field          | Type   | Notes                                                                                                        |
|----------------|--------|--------------------------------------------------------------------------------------------------------------|
| Name           | String | Name of the Item                                                                                             |
| \_id           | String | Same as Name, unique for the system. Lowercase and - instead of space.                                       |
| Source         | String | `Core X.0` for core items, `Core X.0+` for implied core items (Mega stones), or `Homebrew`. X for book version|
| Author         | String | Only required when Source is `Homebrew`. The discord handle or other way of crediting the Homebrew's author. |
| PMD            | Bool   | Flag for if this item is meant for Pokemon Mystery Dungeon games.                                            |
| Pocket         | String | The "Bag Pocket" you would find this item in. A super category.                                              |
| Category       | String | Optional, subcategories within a Pocket.                                                                     |
| Description    | String | Description of the item                                                                                      |
| OneUse         | Bool   | Flag for if the item is consumed on use                                                                      |
| PMDPrice       | String | Only required when PMD flag is true. Price to purchase the item in PMD settings.                             |
| TrainerPrice   | String | Only required when PMD flag is false. Price to purchase the item in Trainer settings.                        |
| ForTypes       | String | Space separated types that the item's effect applies to. Only required for certain items.                    |
| ForPokemon     | String | Space separated pokemon **\_id**'s that the item's effect applies to. Only required for certain items.       |
| HealthRestored | int    | Amount of health restored by the item. Only required when the item heals.                                    |
| Cures          | String | Status conditions cured by the item. Only required when the item heals.                                      |
| Boost          | String | Space separated Attributes that are increased when holding/using this item. Not required.                    |
| Value          | int    | Amount to increase attributes in the Boost field by. Required when Boost is provided.                        |

##### Pocket options:
- HeldItems
- TrainerItems
- EvolutionItem
- Medicine
- Pokeballs