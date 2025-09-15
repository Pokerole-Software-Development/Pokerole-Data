from srd_engine import SRD_Engine
from driver import Driver

# create an Engine

srd = SRD_Engine('/Users/bill/Code/Pokerole SRD', 'v3.0')

# Create a driver using that Engine

driver = Driver(srd)

# Execute

driver.generate_pokedex()
driver.generate_abilities()
driver.generate_images(['ALL'])