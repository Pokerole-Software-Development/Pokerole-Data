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
| HiddenAbility   | String    | Yes   | Ability Name                                                         |
| EventAbilities  | String    | Yes   | Ability Name                                                         |
| RecommendedRank | String    |       | Rank the Species MIGHT be found in the wild                          |
| GenderType      | String    | Yes   | Empty String unless Species has unique gender forms, then "M" or "F" |
| Legendary       | Bool      |       | Flag for Legendaries (Specifically, with max stats by default)       |
| GoodStarter     | Bool      |       | Flag to be set if the good starter symbol is on the Pokedex entry    |
| \_id            | String    |       | Name field, but spaces replaced with '-' and all lowercase           |
| DexCategory     | String    |       | So and So Pokemon label from Pokedex                                 |
| Height          | Object    |       | Height in Feet and Meters. Both Floats.                              |
| Weight          | Object    |       | Weight in Kilograms and Pounds. Both Floats.                         |
| DexDescription  | String    |       | Pokedex flavor text                                                  |
| Evolutions      | List      |       | List of Objects. See Evolution objects below                         |
| Image           | String    |       | Basename for this pokemon's sprites                                  |
| Moves           | List      |       | List of Objects. See Learnset below.                                 |

### Evolution Objects

It's possible to have no Evolution objects in the list. 

| Field   | Data Type | Null? | Notes                                                                            |
| ------- | --------- | ----- | -------------------------------------------------------------------------------- |
| To      | String    |       | The name of a Pokemon this Pokemon evolves into. From/To are mutually exclusive. |
| From    | String    |       | The name of a Pokemon this Pokemon evolves from. From/To are mutually exclusive. |
| Kind    | String    |       | How the Pokemon evolves. (Mega, Level, Stone, etc...)                            |
| Speed   | String    |       | Evolution Speed of a Level based evolution. Only present when kind is Level      |
| Item    | String    |       | Evolution item required for evolution. Only present when kind is requires Item.  |
| Stat    | String    |       | Stat to check for evolution for Stat based evolution                             |
| Value   | String    |       | Stat value to check for evolution via stat based evolution                       |
| Special | String    |       | Other note for evolution                                                         | 

### Learnset Objects

| Field   | Data Type | Null? | Notes                       |
| ------- | --------- | ----- | --------------------------- |
| Learned | String    |       | Rank the move is learned at |
| Name    | String    |       | The name of the Move        | 

## Moves

| Field        | Type   | Notes                                     |
| ------------ | ------ | ----------------------------------------- |
| Name         | String | Name of the Move                          |
| Type         | String | Type of the Move                          |
| Category     | String | Physical, Special, Support                |
| Power        | int    | Power value of the move                   |
| Damage1      | String | Attribute Name or Empty String            |
| Damage2      | String | Second Damage Pool source or Empty String |
| Accuracy1    | String | Attribute Name                            |
| Accuracy2    | String | Skill Name                                |
| Target       | String | What is targeted by Move                  |
| Effect       | String | Move's effect text                        |
| Description  | String | Description text for move                 |
| \_id         | String | Same as Name, unique for the system       |
| Attributes   | Object | Values that are used by Foundry           |
| AddedEffects | Object | Values that are used by Foundry           | 

## Abilities

| Field       | Type   | Notes                               |
| ----------- | ------ | ----------------------------------- |
| \_id        | String | Same as Name, unique for the system |
| Name        | String | Name of Ability                     |
| Effect      | String | Effect text of Ability              |
| Description | String | Flavor Text description of Ability  |


## Natures

| Field       | Type   | Notes                                             |
| ----------- | ------ | ------------------------------------------------- |
| \_id        | String | Same as Name, unique for the system               |
| Name        | String | Name of Nature                                    |
| Nature      | String | Name and Confidence in format "Name (confidence)" |
| Confidence  | int    | Confidence score of the Nature                    |
| Description | String | Text Description of Nature                        |
| Keywords    | String | Comma separated keywords for the Nature           |

