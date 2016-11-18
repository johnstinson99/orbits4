# Calculate orbit using Newton's law of Universal Gravitation
# Demonstrates interesting effects when run.
#
# requires the tkinter.py library (tk) to run.
# rewritten from graphics.py as tkinter.py is available in the Anaconda 3.5 Python distribution


from math import pi  # import pi from math library rather than defining ourselves
from src.celestial_body import Body
from src.universe_model import UniverseModel

my_universe_model = UniverseModel()

# Set up basic parameters
star1 = Body(name='Star 1', mass=1.47e30, radius=10, colour='orange', universe_model=my_universe_model)
star2 = Body(name='Star 2', mass=8.11e29, radius=6, colour='red', universe_model=my_universe_model)  # 8.11e29,
planet = Body(name='Planet', mass=5.26e5, radius=4, colour='green', universe_model=my_universe_model)
my_body_list = [star1, star2, planet]


def set_initial_x_coordinates():
    # set initial x coordinates (initial ys are all zero as planets in horizontal line)
    star1.x_old = star1.x = 0  # put star 1 (the one on the left) at origin of universe (not origin of screen)
    planet.x_old = planet.x = star1.get_habitable_distance()  # put the planet a habitable distance away
    star2.x_old = star2.x = 10 * planet.x  # put star 2, 10 times the orbit away.


def scenario2_two_equal_mass_stars_circling_in():
    star2.mass = 1.47e30
    my_body_list.remove(planet)
    # star2.y += 1e10
    star2.x_old = star2.x = 2.5 * planet.x  # put star 2, 10 times the orbit away.


def scenario3_stars_close_together():
    star2.x_old = star2.x = 2.5 * planet.x  # put star 2, 10 times the orbit away.


def scenario4_two_unequal_mass_stars_circling_in():
    # star2.mass = 1.47e30
    my_body_list.remove(planet)
    # star2.y += 1e10
    star2.x_old = star2.x = 5.0 * planet.x  # put star 2, 10 times the orbit away.


def scenario5_stars_very_close_together():
    star2.x_old = star2.x = 2 * planet.x  # put star 2, 10 times the orbit away.

def scenario6_stars_v_v_close_together():
    star2.x_old = star2.x = 1.50026 * planet.x  # put star 2, 10 times the orbit away.


def set_x_velocities():
    # Barycentre is the centre of mass betweeen two objects
    # https://en.wikipedia.org/wiki/Barycenter
    # my_barry_centre = (star2.mass * star2.x) / (star1.mass + star2.mass)  # BaryCentreA = (m[1]*x[1]) / (m[0]+m[1])
    my_barry_centre = my_universe_model.get_barry_centre()
    print('barry_centre = ' + str(my_barry_centre))
    # planets all start in horizontal line, so x velocities are all zero to start.
    star1.vy = my_barry_centre / ((star2.x ** 3) / (UniverseModel.G * (star1.mass + star2.mass))) ** 0.5
    star2.vy = -((star2.x - my_barry_centre) / ((star2.x ** 3) / (UniverseModel.G * (star1.mass + star2.mass))) ** 0.5)
    planet.vy = star1.vy + ((UniverseModel.G * star1.mass) / planet.x) ** 0.5

my_universe_model.setup(body_list=my_body_list)
set_initial_x_coordinates()
# scenario2_two_equal_mass_stars_circling_in()  # scenario depends on initial x coords being setup
scenario6_stars_v_v_close_together()
# scenario4_two_unequal_mass_stars_circling_in()
set_x_velocities()  # velocities depend on barry_centre (model.setup), mass and distance (updated in scenario)

while True:
    my_universe_model.update_position_and_velocity_and_screen_after_delta_t()
