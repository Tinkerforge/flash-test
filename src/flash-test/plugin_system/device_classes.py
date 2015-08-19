from .plugins.bricklet_ambient_light_v2 import Plugin as bricklet_ambient_light_v2_class
from .plugins.bricklet_moisture import Plugin as bricklet_moisture_class
from .plugins.bricklet_remote_switch import Plugin as bricklet_remote_switch_class
from .plugins.bricklet_rs232 import Plugin as bricklet_rs232_class

device_classes = [
    bricklet_ambient_light_v2_class,
    bricklet_moisture_class,
    bricklet_remote_switch_class,
    bricklet_rs232_class,
]
