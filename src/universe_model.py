from tkinter import *


class UniverseModel:

    G = 6.67408e-11  # G is the gravitational constant (as opposed to g which is gravity on earth)
    dt = 3e3  # time simulated between two frames, in seconds - try ne4
    # waitTime = 1e-3  # actual time between two displayed frames - try ne-3
    scale = 4e-10  # multiplier to convert metres to pixels on screen - try ne-10

    def __init__(self, screen_width_pixels=800, screen_height_pixels=800):
        self.screen_width_pixels = screen_width_pixels
        self.screen_height_pixels = screen_height_pixels
        self.body_list = []
        self.my_canvas = None  # can only declare instance variables in __init__ but unittests don't need canvas.
        self.time_now_seconds = 0
        self.barycentre = None
        self.centre_x = 0
        self.centre_y = 0
        self.count = 0

    def setup(self, body_list):
        master = Tk()
        self.body_list = body_list  # need bodylist before calculating barycentre
        self.my_canvas = Canvas(master, width=self.screen_width_pixels, height=self.screen_height_pixels)
        self.my_canvas.pack()
        self.my_canvas.create_rectangle(0, 0, master.winfo_screenwidth(), master.winfo_screenheight(), fill="black")
        self.my_canvas.update()
        self.barycentre = self.get_barycentre()
        self.centre_x = self.barycentre * UniverseModel.scale
        for body in self.body_list:
            print(body)

    def get_barycentre(self):
        return UniverseModel.get_barycentre_for_body_list(self.body_list)  # done this way to make it easier to test

    @staticmethod
    def get_barycentre_for_body_list(my_list):
        # Finds the barycentre of ALL the bodies using (m0*x0 + m1*x1 + m2*x2 ) / (m0 + m1 + m2)
        numerator = sum(body.mass * body.x for body in my_list)
        denominator = sum(body.mass for body in my_list)
        return numerator/denominator

    def screen_x_from_real_x(self, real_x):
        return real_x * UniverseModel.scale + self.screen_width_pixels / 2 - self.centre_x

    def screen_y_from_real_y(self, real_y):
        return real_y * UniverseModel.scale + self.screen_width_pixels / 2 - self.centre_y

    def draw_line_from_old_to_new_position(self, a_body):
        self.my_canvas.create_line(self.screen_x_from_real_x(a_body.x_old),
                                   self.screen_y_from_real_y(a_body.y_old),
                                   self.screen_x_from_real_x(a_body.x),
                                   self.screen_y_from_real_y(a_body.y),
                                   fill=a_body.colour)

        # remember old x and y for next time we draw a line.
        a_body.x_old = a_body.x
        a_body.y_old = a_body.y

    @staticmethod
    def acceleration_tuple_on_body_caused_by_body_list(a_body, list_of_other_bodies):
        ax = ay = 0  # start with acceleration of zero, then work out impact of each of the other bodies on acceleration
        for other_body in list_of_other_bodies:
            # Find x and y distances between bodies
            my_body_to_other_body_x = a_body.x - other_body.x
            my_body_to_other_body_y = a_body.y - other_body.y

            # use Pythagoras to find the scalar distance
            my_body_to_other_body_dist = (my_body_to_other_body_x**2 + my_body_to_other_body_y**2)**0.5

            # Work out the force between two bodies using the gravitational constant G
            force = -((UniverseModel.G * a_body.mass * other_body.mass) / (my_body_to_other_body_dist ** 2))

            # Work out the magnitude of acceleration using F = ma
            a = force / a_body.mass

            # Work out x and y components of acceleration
            ax += (my_body_to_other_body_x/my_body_to_other_body_dist) * a
            ay += (my_body_to_other_body_y/my_body_to_other_body_dist) * a
        my_acceleration_tuple = (ax, ay)
        return my_acceleration_tuple

    def update_position_and_velocity_and_screen_after_delta_t(self):
        for my_body in self.body_list:
            # work out the x and y components of acceleration on my_body,
            # caused by each of the other bodies, then sum.
            other_bodies = self.body_list.copy()
            other_bodies.remove(my_body)
            acceleration_tuple = UniverseModel.acceleration_tuple_on_body_caused_by_body_list(my_body, other_bodies)

            # my_body.test_method(acceleration_tuple)
            my_body.update_velocity_and_position_from_acceleration_tuple(acceleration_tuple, UniverseModel.dt)

            if self.count % 100 == 0:  # draw a line every n moves
                self.draw_line_from_old_to_new_position(my_body)

            if self.count % 10000 == 0:  # update screen every n moves
                self.my_canvas.update()

        # time.sleep(waitTime)
        self.count += 1
        self.time_now_seconds += UniverseModel.dt
