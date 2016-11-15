from graphics import *


class Body:
    def __init__(self,
                 mass=0,
                 name='Body with no name yet',
                 radius=0,
                 colour='',
                 display_window=None):

        self.mass = mass        # mass of body in kg
        self.name = name
        self.radius = radius    # radius of displayed bodies in pixels - for aesthetic purposes only
        self.colour = colour
        self.display_window = display_window

        # circle has a move method, so hold onto one instance
        # of a circle and keep moving it rather than creating a new one each time.
        self.circle = Circle(Point(0, 0), 0)
        self.x = 0
        self.y = 0
        self.x_old = 0
        self.y_old = 0
        self.vx = 0  # velocity in x direction
        self.vy = 0  # velocity in y direction

    def update_velocity_and_position_from_acceleration_tuple(self, acceleration_tuple, dt, scale):
        (ax, ay) = acceleration_tuple

        # find velocity from acceleration
        self.vx += (ax * dt)  # v = u + a*t
        self.vy += (ay * dt)

        # find x and y position from velocity
        dx = self.vx * dt
        dy = self.vy * dt

        # update x and y and moves the circle object
        self.x += dx
        self.y += dy
        #self.circle.move(dx*scale, dy*scale)  # remove circle drawing to speed up simlation

    def __str__(self):  # the __str__() method is called by the print() method
        return(self.name +
               ", mass: " + str(self.mass) +
               ", radius: " + str(self.radius) +
               ", colour: " + str(self.colour) +
               ", x: " + str(self.x) +
               ", x_old: " + str(self.x_old) +
               ", vx: " + str(self.vx) +
               ", y: " + str(self.y) +
               ", y_old: " + str(self.y_old) +
               ", vy: " + str(self.vy)
               )
