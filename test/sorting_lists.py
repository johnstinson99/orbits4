my_list = ['a', 'B', 'A', 'b']
my_list.sort()
my_list.sort(key=str.lower)
print(my_list)

def print_bodies(my_bodies):
    for my_body in my_bodies:
        print (my_body.name, my_body.mass)

from src.celestial_body import Body
body1 = Body(name='body1', mass = 3)
body2 = Body(name='body2', mass = 5)
body3 = Body(name='body3', mass = 4)
body_list = [body1, body2, body3]
print_bodies(body_list)


def body_mass(a_body):
    return a_body.mass

body_list.sort(key=body_mass, reverse=True)
body_list.sort(key=Body.mass, reverse=True)
body_list.sort(key=lambda body: body.mass)
print_bodies(body_list)

print(str.lower("HI"))
print(Body.mass(body1))
