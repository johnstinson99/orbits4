from tkinter import *

master = Tk()

my_canvas = Canvas(master, width=800, height=800)
my_canvas.pack()

my_canvas.create_rectangle(0, 0, master.winfo_screenwidth(), master.winfo_screenheight(), fill="black")  # black background

my_list = [0, 0, 200, 100]
my_canvas.create_line(my_list)
my_canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
my_oval = my_canvas.create_oval(100, 100, 200, 200, fill="red")

oval_coords = [100, 100, 200, 200]  #documentation says tuple, but using a list allows us to update in place.

while True:
    my_canvas.update()
    oval_coords = [coord + 1 for coord in oval_coords]
    # my_canvas.create_line(0, 0, 200, 100)
    my_canvas.coords(my_oval, oval_coords)  # change coordinates
# mainloop()  # defined in __init__ of tkinter.  Runs the main loop of tcl.

class Circle:
    def __init__(self, x_centre, y_centre, radius):
        self.x0 = x_centre - radius
        self.x1 = x_centre + radius
        self.y0 = y_centre - radius
        self.y1 = y_centre + radius

