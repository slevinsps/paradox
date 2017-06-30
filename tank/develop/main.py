# Imports as usual
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.layer import ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
import math
from cocos.text import Label
from cocos.actions import Driver
from pyglet.window import key
from pyglet.window import mouse

director.init(width=800, height=600, autoscale=False, resizable=True)

keyboard = key.KeyStateHandler()

scroller = ScrollingManager()


# Here's something you haven't scene before!
# We'll be using the Driver class from the "move_actions" provided by Cocos, and editing it slightly for our needs
# The driver class is built to help make having sprites behave like vehicles much simpler
class CarDriver (Driver):
    def step(self, dt):
        self.target.rotation += (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 100 * dt

        self.target.acceleration = (keyboard[key.UP] - keyboard[key.DOWN]) * 350

        if keyboard[key.SPACE]:
            self.target.speed = 0

        super(CarDriver, self).step(dt)

        scroller.set_focus(self.target.x, self.target.y)


class MouseInput(ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super(MouseInput, self).__init__()

        # This time I set variables for the position rather than hardcoding it
        # I do this because we will want to alter these values later
        self.position_x = 100
        self.position_y = 240

        # Once again I make a label
        self.text = Label("No mouse interaction yet",
                          font_name = "Helvetica",
                          font_size = 24,
                          x = self.position_x,
                          y = self.position_y)

        # Then I just add the text!

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite("tank_pushka.png")

        self.sprite.position = 200, 100

        # Then we add it
        self.add(self.sprite)
        self.add(self.text)

    # Like last time we need to make a function to update that self.text label to display the mouse data
    def update_text(self, mouse_x_pos, mouse_y_pos):
        # I make a text variable and store a string containing the x and y positions passed into the function
        text = 'Mouse is at %d,%d' % (mouse_x_pos, mouse_y_pos)

        # Next I simply do what I did for the keyboard and update the self.text label to contain our new string
        self.text.element.text = text

        # I also update its now dynamic position by moving the text to wherever the user clicks
        #self.text.element.x, self.text.element.y = self.position_x, self.position_y
        if (self.sprite.y < self.position_y):
            self.sprite.rotation = math.degrees(
                math.atan((self.sprite.x - self.position_x)/(self.sprite.y - self.position_y)))
        elif (self.sprite.y > self.position_y):
            self.sprite.rotation = math.degrees(
                math.atan((self.sprite.x - self.position_x) / (self.sprite.y - self.position_y)))+180

        #self.sprite.x, self.sprite.y = self.position_x, self.position_y

        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        # self.sprite.do(MouseInput())

    # Also similarly to the keyboard, I overload a few default functions that do nothing
    # I make all of them update the text, and I make clicks update both the text and the label's position
    def on_mouse_motion(self, x, y, dx, dy):
        self.update_text(x, y)
        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        # This next line seems a bit odd, and that's because it is!
        self.position_x, self.position_y = director.get_virtual_coordinates(x, y)
        # It introduces a new topic, virtual coordinates
        # If I had used default coordinates, the position might be updated in the OS's coordinates rather than the scene
        # The director provides us with the appropriate coordinates within our "virtual" window

        self.update_text(x, y)


# Now we need to make a layer for the car itself!
# Remember that the layer needs to be scrollable so that the car can move around the map
class CarLayer(ScrollableLayer):
    def __init__(self):
        super(CarLayer, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite("tank_telo.png")

        # We set the position (standard stuff)
        self.sprite.position = 200, 100

        # Oh no! Something new!
        # We set a maximum forward and backward speed for the car so that it doesn't fly off the map in an instant
        self.sprite.max_forward_speed = 200
        self.sprite.max_reverse_speed = -100

        # Then we add it
        self.add(self.sprite)

        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        self.sprite.do(CarDriver())

class tankPushkaLayer(ScrollableLayer):
    def __init__(self):
        super(tankPushkaLayer, self).__init__()

        # Here we simply make a new Sprite out of a car image I "borrowed" from cocos
        self.sprite = Sprite("tank_pushka.png")

        # We set the position (standard stuff)
        self.sprite.position = 200, 100

        # Oh no! Something new!
        # We set a maximum forward and backward speed for the car so that it doesn't fly off the map in an instant
        self.sprite.max_forward_speed = 200
        self.sprite.max_reverse_speed = -100

        # Then we add it
        self.add(self.sprite)

        # And lastly we make it do that CarDriver action we made earlier in this file (yes it was an action not a layer)
        #self.sprite.do(MouseInput())

car_layer = CarLayer()
#tank_pushka_layer = tankPushkaLayer()
MouseInput_layer = MouseInput()

map_layer = load("road.tmx")["map0"]

scroller.add(map_layer)
scroller.add(car_layer)
#scroller.add(tank_pushka_layer)
scroller.add(MouseInput_layer)

scene = Scene(scroller)

director.window.push_handlers(keyboard)

# And finally we run the scene
director.run(scene)

# Now our games are actually starting to seem like, well, games!