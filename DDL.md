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

| Field              | Type   | Notes                                                                |
| ------------------ | ------ | -------------------------------------------------------------------- |
| \_id               | String | Same as Name, Unique ID for the system.                              |
| Number             | int    | Pokedex Number of Species                                            |
| DexID              | String | Pokedex Number + variant flags, if any                               |
| Name               | String | Pokemon Species name                                                 |
| Type1              | String | Type                                                                 |
| Type2              | String | Type or empty string                                                 |
| BaseHP             | int    | Base HP value                                                        |
| Strength           | int    | Base Strength score for the Species                                  |
| MaxStrength        | int    | Max Strength score for the Species                                   |
| Dexterity          | int    | Base Dexterity score for the Species                                 |
| MaxDexterity       | int    | Max Dexterity score for the Species                                  |
| Vitality           | int    | Base Vitality score for the Species                                  |
| MaxVitality        | int    | Max Vitality score for the Species                                   |
| Special            | int    | Base Special score for the Species                                   |
| MaxSpecial         | int    | Max Special score for the Species                                    |
| Insight            | int    | Base Insight score for the Species                                   |
| MaxInsight         | int    | Max Insight score for the Species                                    |
| Ability1           | String | Ability Name                                                         |
| Ability2           | String | Ability Name or empty string if none                                 |
| HiddenAbility      | String | Ability Name or empty string if none                                 |
| EventAbilities     | String | Ability Name or empty string if none                                 |
| Unevolved          | Bool   |                                                                      |
| HasForm            | String | "Yes" or Empty String                                                |
| RecommendedRank    | String | Rank the Species MIGHT be found in the wild                          |
| GenderType         | String | Empty String unless Species has unique gender forms, then "M" or "F" |
| Legendary          | Bool   |                                                                      |
| Sprite             | String | Basename for this pokemon's sprites                                  |
| GoodStarter        | Bool   |                                                                      |
| Learnset           | String | Name of Learnset document for the Pokemon                            |
| Abilities          | String | Combined Abilities in format "#1 / #2 (Hidden) \<Event\>"            |
| Types              | String | Combined Type1 and Type2, " / " separated if both                    |
| DexCategory        | String | So and So Pokemon label from Pokedex                                 |
| Height             | Object | Height in Deimeters, Feet, and Meters                                |
| Weight             | Object | Height in Hectogram, Kilograms, and Pounds                           |
| DexDescription     | String | Pokedex flavor text                                                  |
| Baby               | String | "Yes" or "No" for if the Pokemon is considered a Baby mon            |
| PrimaryEggGroup    | String | Egg group of Pokemon                                                 |
| SecondaryEggGroup  | String | Egg group of Pokemon or empty string if no Secondary                 |
| BookImageName      | String | Name of the Regular Pokemon image from the book                      |
| BookShinyImageName | String | Name of the Shiny Pokemon image from the book                        |

*Note: The last column "When Querying Use:" is only relevant for the columns that don't have dashes.*

## Learnsets

| Field   | Type   | Notes                                                                                                                      |
| ------- | ------ | -------------------------------------------------------------------------------------------------------------------------- |
| Name    | String | Same as Name, unique for the system                                                                                        |
| Name    | String | Name of Mon                                                                                                                |
| Species | String | same as Name                                                                                                               |
| DexID   | String | Pokedex Number + variant flags, if any                                                                                     |
| Moves   | List   | List of Objects. Each Object has `Learned (String)` with the rank the move is learned at and `Name (String)` of that move. |

## Moves

| Field       | Type   | Notes                                     |
| ----------- | ------ | ----------------------------------------- |
| \_id        | String | Same as Name, unique for the system       |
| Name        | String | Name of the Move                          |
| Type        | String | Type of the Move                          |
| DmgType     | String | "Physical" or "Special"                   |
| Power       | int    | Power value of the move                   |
| Damage1     | String | Attribute Name or Empty String            |
| Damage2     | String | Second Damage Pool source or Empty String |
| Accuracy1   | String | Attribute Name                            |
| Accuracy2   | String | Skill Name                                |
| Target      | String | What is targeted by Move                  |
| Description | String | Description text for move                 |
| Effect      | String | Move's effect text                        |

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

