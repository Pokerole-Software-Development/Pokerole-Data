from srd_engine import SRD_Engine
from driver import Driver

# create an Engine

srd = SRD_Engine('/Users/bill/Code/Pokerole SRD', 'v3.0')
# fndry = SRD_Engine('../../FoundryModule', 'v2.0', foundry_version='0.3.1')

# Create a driver using that Engine

driver = Driver(srd)
# driver = Driver(fndry)

# Execute

driver.generate_pokedex()
driver.generate_abilities()
driver.generate_moves()
driver.generate_items()
driver.generate_natures()
driver.generate_images(['ALL'])