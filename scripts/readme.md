# Data Translations

While the Dataset is great on it's own, it's true purpose is to be translated into other formats to power other Pokerole applications. The two primary examples of applications driven by this Dataset are the Pokerole Foundry Module and the Obsidian System Reference Document. 

Scripts designed to manipulate the Dataset are built from the `Databuilder.py` class. This class standardizes how the data and paths are managed for ease of us. It leverages the Python Fire library to be operated via the command line. `foundry-db.py` and `srd-db.py` are instantiations of the databuilder designed for each of those projects. 

All executions of Databuilders begin with `python <filename.py>`. To configure the databuilder on the fly, various parameters can be set on the command line. These take the format of `--parameter_name="parameter value"`. These parameters are detailed below. 

## Class Level Parameters 

The following are parameters that can be provided to both scripts:

| Parameter | Description                                                               | Default |
|-----------|---------------------------------------------------------------------------|---------|
| root      | The root of the Dataset the Databuilder is reading from                   | ../     |

These parameters can be provided to `srd-db.py`.

| Parameter | Description                                                                                       | Default |
|-----------|---------------------------------------------------------------------------------------------------|---------|
| version   | Subfolder in the root to pull data from for when there are multiple sets.                         | v2.0    |
| obsidian  | The Obsidian output folder. The SRD is created in `Pokerole SRD/SRD {Version}` under this folder. |         |

These parameters can be provided to `foundry-db.py`.

| Parameter        | Description                                                                               | Default |
|------------------|-------------------------------------------------------------------------------------------|---------|
| pokerole_version | Subfolder in the root to pull data from for when there are multiple sets. Same as Version | v2.0    |
| system_version   | Foundry system version to use.                                                            | 0.3.1   |
| foundry_dir      | The path to the Data/systems/pokerole folder in your foundry installation                 |         |

## Update

The main function of Databuilders is the `update` function. Update is the same between all Databuilders and has one required parameter. 

| Parameter | Description                                                                                                | Default |
|-----------|------------------------------------------------------------------------------------------------------------|---------|
| *argv     | any number of builders to run. A builder is a function in the file that starts with `build_`               |         |
| batch     | A flag tells the builder to run all the builder functions without listing them out. entered like `--batch` | False   |
| confirm   | Skips the Y/N check on each build function before running. entered like `--confirm`.                       | False   |

## Putting it Together

`python foundry-db.py --foundry_dir="/Users/person/Library/Application Support/FoundryVTT/Data/systems/pokerole" --pokerole_version=v2.0 update items`

`python foundry-db.py --pokerole_version=v2.0 update --batch --confirm`

`python srd-db.py update --batch --confirm`