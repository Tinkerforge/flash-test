from .plugins.brick_imu_v2 import Plugin as brick_imu_v2_class
from .plugins.bricklet_accelerometer import Plugin as bricklet_accelerometer_class
from .plugins.bricklet_ambient_light_v2 import Plugin as bricklet_ambient_light_v2_class
from .plugins.bricklet_load_cell import Plugin as bricklet_load_cell_class
from .plugins.bricklet_moisture import Plugin as bricklet_moisture_class
from .plugins.bricklet_remote_switch import Plugin as bricklet_remote_switch_class
from .plugins.bricklet_rs232 import Plugin as bricklet_rs232_class

device_classes = [
    brick_imu_v2_class,
    bricklet_accelerometer_class,
    bricklet_ambient_light_v2_class,
    bricklet_load_cell_class,
    bricklet_moisture_class,
    bricklet_remote_switch_class,
    bricklet_rs232_class,
]
