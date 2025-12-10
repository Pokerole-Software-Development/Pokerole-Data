from srd_engine import SRD_Engine
from foundry_engine import Foundry_Engine
from driver import Driver
from fire import Fire

SRD_FOLDER = '' # The SRD will be placed in a "Pokerole SRD" in this folder.
GAME_VERSION = 'v3.0' # Or make it 'v2.0'


def buildSRD(game_version, srd_folder):
    srd = SRD_Engine(srd_folder, game_version)
    driver = Driver(srd)

    driver.generate_abilities()
    driver.generate_moves()
    driver.generate_items()
    driver.generate_pokedex()
    driver.generate_natures()
    driver.generate_images(['BookSprites', 'HomeSprites', "ItemSprites"])

def buildFoundry(game_version, foundry_version='3.348'):
    fndry = Foundry_Engine('../../FoundryModule', game_version, foundry_version)
    driver = Driver(fndry)

    driver.generate_abilities()
    driver.generate_moves()
    driver.generate_items()
    driver.generate_pokedex()
    driver.generate_images(['BookSprites', "ItemSprites"])

if __name__ == '__main__':
  Fire()