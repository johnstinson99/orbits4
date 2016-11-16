from src.universe_model import UniverseModel


class Body:
    def __init__(self,
                 mass=0,
                 name='Body with no name yet',
                 radius=0,
                 colour='',
                 universe_model=None):

        self.mass = mass        # mass of body in kg
        self.name = name
        self.radius = radius    # radius of displayed bodies in pixels - for aesthetic purposes only
        self.colour = colour
        self.model = universe_model

        # circle has a move method, so hold onto one instance
        # of a circle and keep moving it rather than creating a new one each time.
        # self.circle = Circle(Point(0, 0), 0)
        self.x_old = self.x = 0
        self.y_old = self.y = 0
        self.vx_old = self.vx = 0  # velocity in x direction
        self.vy = 0  # velocity in y direction
        self.previous_orbit_start_time_seconds = 0
        self.orbital_period_seconds = 0  # start wih 0 rather than None to avoid exceptions
        self.orbit_count = 0

    def get_orbital_period_seconds(self):
        return self.orbital_period_seconds

    def get_orbital_period_earth_days(self):
        return self.get_orbital_period_seconds()/(60*60*24)

    def get_orbital_period_earth_years(self):
        return self.get_orbital_period_earth_days()/365.25

    def start_new_orbit(self):
        self.orbital_period_seconds = self.model.time_now_seconds - self.previous_orbit_start_time_seconds
        self.previous_orbit_start_time_seconds = self.model.time_now_seconds
        if self.orbit_count > 0:
            print(self.name, "orbit_count = ", self.orbit_count, "orbital_period =", "{:.2f}".format(self.get_orbital_period_earth_days()), "earth days")
        self.orbit_count += 1

    def check_if_orbit_complete_and_update_orbital_period_if_so(self):
        if self.vx > 0 and not self.vx_old > 0:  # New orbit starts if x velocity switches from -ve to +ve
            self.start_new_orbit()

    def update_velocity_and_position_from_acceleration_tuple(self, acceleration_tuple, dt):
        (ax, ay) = acceleration_tuple
        # find velocity from acceleration
        self.vx_old = self.vx  # used in calculation of orbital period

        self.vx += (ax * dt)  # v = u + a*t
        self.vy += (ay * dt)

        # find x and y position from velocity
        dx = self.vx * dt
        dy = self.vy * dt

        # update x and y and move the circle object
        self.x += dx
        self.y += dy
        # self.circle.move(dx*scale, dy*scale)  # remove circle drawing to speed up simulation

        self.check_if_orbit_complete_and_update_orbital_period_if_so()

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
