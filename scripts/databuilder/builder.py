from srd_engine import SRD_Engine
from foundry_engine import Foundry_Engine
from driver import Driver

srd = SRD_Engine('/Users/bill/Code/Pokerole SRD', 'v2.0')
driver = Driver(srd)

driver.generate_abilities()
driver.generate_moves()
driver.generate_items()
driver.generate_pokedex()
driver.generate_natures()

srd = SRD_Engine('/Users/bill/Code/Pokerole SRD', 'v3.0')
driver = Driver(srd)

driver.generate_abilities()
driver.generate_moves()
driver.generate_items()
driver.generate_pokedex()
driver.generate_natures()
driver.generate_images('BookSprites', 'HomeSprites', "ItemSprites")

# --------------------------------------------------------------------------

fndry = Foundry_Engine('../../FoundryModule', 'v3.0', foundry_version='3.348')
driver = Driver(fndry)

driver.generate_abilities()
driver.generate_moves()
driver.generate_items()
driver.generate_pokedex()
driver.generate_images(['ALL'])
