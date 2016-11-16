# Calculate orbit using Newton's law of Universal Gravitation
# Demonstrates interesting effects when run.
#
# requires the tkinter.py library (tk) to run.
# rewritten from graphics.py as tkinter.py is available in the Anaconda 3.5 Python distribution


from math import pi  # import pi from math library rather than defining ourselves
from src.celestial_body import Body
from src.universe_model import UniverseModel

my_universe_model = UniverseModel()

star1 = Body(name='Star 1', mass=1.47e30, radius=10, colour='orange', universe_model=my_universe_model)
star2 = Body(name='Star 2', mass=1.47e30, radius=6, colour='red', universe_model=my_universe_model)  # 8.11e29,
planet = Body(name='Planet', mass=5.26e5, radius=4, colour='green', universe_model=my_universe_model)

# Luminosity of star 1 relative to the sun - used to find the nearest habitable distance
L = (star1.mass / 1.989e30) ** 3

# set initial x coordinates (initial ys are all zero as planets in horizontal line)
star1.x_old = star1.x = 0  # put star 1 (star about which planet rotates) at origin of universe (not origin of screen)
planet.x_old = planet.x = (L**0.5) * 1.496e11  # put the planet a habitable distance away
star2.x_old = star2.x = 2.5 * planet.x  # put star 2, 10 times the orbit away.

# Barycentre is the centre of mass betweeen two objects
# https://en.wikipedia.org/wiki/Barycenter
my_barry_centre = (star2.mass * star2.x) / (star1.mass + star2.mass)  # BaryCentreA = (m[1]*x[1]) / (m[0]+m[1])
print('barry_centre = ' + str(my_barry_centre))

# planets all start in horizontal line, so x velocities are all zero to start.
star1.vy = my_barry_centre / ((star2.x ** 3) / (UniverseModel.G * (star1.mass + star2.mass))) ** 0.5
star2.vy = -((star2.x - my_barry_centre) / ((star2.x ** 3) / (UniverseModel.G * (star1.mass + star2.mass))) ** 0.5)
planet.vy = star1.vy + ((UniverseModel.G * star1.mass) / planet.x) ** 0.5


my_universe_model.setup(body_list=[star1, star2], barry_centre=my_barry_centre)

star2.y += 1e10

while True:
    my_universe_model.update_position_and_velocity_and_screen_after_delta_t()
