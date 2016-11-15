# Calculate orbit using Newton's law of Universal Gravitation
# Demonstrates interesting effects when run.
#
# To run, this requires the following library
# http://mcsp.wartburg.edu/zelle/python/graphics.py
# to be copied to
# C:\Users\<user>\Anaconda3\envs\<my_env>\Lib or equivalent.
# the graphics.py package  has a dependency on tk (tkinter)


from graphics import *
from math import pi  # import pi from math library rather than defining ourselves
from src.celestial_body4 import Body

G = 6.67408e-11  # G is the gravitational constant (as opposed to g which is gravity on earth)
screen_width_pixels = 600
screen_height_pixels = 600

win = GraphWin('OrbitCalculator', screen_width_pixels, screen_height_pixels)
win.setBackground('black')

# input data here:
dt = 2e4  # time simulated between two frames, in seconds - try ne4
waitTime = 1e-3  # actual time between two displayed frames - try ne-3
scale = 4e-10  # multiplier to convert metres to pixels on screen - try ne-10

star1 = Body(name='Star 1',
             mass=1.47e30,
             radius=10,
             colour='orange',
             display_window=win)

star2 = Body(name='Star 2',
             mass=1.47e30,  # 8.11e29,
             radius=6,
             colour='red',
             display_window=win)

planet = Body(name='Planet',
              mass=5.26e5,
              radius=4,
              colour='green',
              display_window=win)

body_list = [star1, star2, planet]

# Luminosity of star 1 relative to the sun - used to find the nearest habitable distance
L = (star1.mass / 1.989e30) ** 3

# set initial x coordinates (initial ys are all zero as planets in horizontal line)
star1.x_old = star1.x = 0  # put star 1 (star about which planet rotates) at origin of universe (not origin of screen)
planet.x_old = planet.x = (L**0.5) * 1.496e11  # put the planet a habitable distance away
star2.x_old = star2.x = 2.5 * planet.x  # put star 2, 10 times the orbit away.

# planet.mass *= 1e22

# Barycentre is the centre of mass betweeen two objects
# https://en.wikipedia.org/wiki/Barycenter
barry_centre = (star2.mass * star2.x) / (star1.mass + star2.mass)  # BaryCentreA = (m[1]*x[1]) / (m[0]+m[1])
print('barry_centre = ' + str(barry_centre))

# planets all start in horizontal line, so x velocities are all zero to start.
star1.vy = barry_centre / ((star2.x ** 3) / (G * (star1.mass + star2.mass))) ** 0.5
star2.vy = -((star2.x - barry_centre) / ((star2.x ** 3) / (G * (star1.mass + star2.mass))) ** 0.5)
planet.vy = star1.vy + ((G * star1.mass) / planet.x) ** 0.5

for body in body_list:
    print(body)

# work out planet orbital periods
year = 2*pi*planet.x/planet.vy  # circumference over velocity (star1 starts at 0,0) - assumes circular orbit
print('Year: ', year/(60*60*24), 'Earth days')  # secs in minute * mins in hour * hours in day
tStars1 = ((2 * pi * barry_centre) / star1.vy) / (60 * 60 * 24 * 365.25)
tStars2 = ((2 * pi * barry_centre) / star1.vy) / year
print('Star orbital period:', tStars1, 'Earth years or', tStars2, 'planet years')

centre_x = barry_centre * scale
centre_y = 0

body_list.remove(planet)
star2.y += 1e10


def screen_x_from_real_x(real_x):
    return real_x * scale + screen_width_pixels / 2 - centre_x


def screen_y_from_real_y(real_y):
    return real_y * scale + screen_width_pixels / 2 - centre_y


def setup_body_circle(a_body):
    screen_x = screen_x_from_real_x(body.x)
    screen_y = screen_y_from_real_y(body.y)
    a_body.circle = Circle(Point(screen_x, screen_y), a_body.radius)
    a_body.circle.setFill(a_body.colour)
    a_body.circle.setOutline(a_body.colour)
    # a_body.circle.draw(win)

for body in body_list:
    setup_body_circle(body)


def draw_line_from_old_to_new_position(a_body):
    line = Line(
            Point(a_body.x_old * scale + screen_width_pixels / 2 - centre_x,
                  a_body.y_old * scale + screen_height_pixels / 2 - centre_y),
            Point(a_body.x * scale + screen_width_pixels / 2 - centre_x,
                  a_body.y * scale + screen_height_pixels / 2 - centre_y))
    line.setOutline(a_body.colour)
    line.draw(win)

    # remember old x and y for next time we draw a line.
    a_body.x_old = a_body.x
    a_body.y_old = a_body.y


def acceleration_tuple_on_body_caused_by_body_list(a_body, list_of_other_bodies):
    ax = ay = 0  # start with acceleration of zero, then work out impact of each of the other bodies on acceleration
    for other_body in list_of_other_bodies:
        # Find x and y distances between bodies
        my_body_to_other_body_x = a_body.x - other_body.x
        my_body_to_other_body_y = a_body.y - other_body.y

        # use Pythagoras to find the scalar distance
        my_body_to_other_body_dist = (my_body_to_other_body_x**2 + my_body_to_other_body_y**2)**0.5

        # Work out the force between two bodies using the gravitational constant G
        force = -((G * a_body.mass * other_body.mass) / (my_body_to_other_body_dist ** 2))

        # Work out the magnitude of acceleration using F = ma
        a = force / a_body.mass

        # Work out x and y components of acceleration
        ax += (my_body_to_other_body_x/my_body_to_other_body_dist) * a
        ay += (my_body_to_other_body_y/my_body_to_other_body_dist) * a
    my_acceleration_tuple = (ax, ay)
    return my_acceleration_tuple

count = 0
while True:
    for my_body in body_list:
        # work out the x and y components of acceleration on my_body,
        # caused by each of the other bodies, then sum.
        other_bodies = body_list.copy()
        other_bodies.remove(my_body)
        acceleration_tuple = acceleration_tuple_on_body_caused_by_body_list(my_body, other_bodies)

        # my_body.test_method(acceleration_tuple)
        my_body.update_velocity_and_position_from_acceleration_tuple(acceleration_tuple, dt, scale)

        if count % 20 == 0:  # draw a line every 20 moves
            draw_line_from_old_to_new_position(my_body)

    # time.sleep(waitTime)
    count += 1
