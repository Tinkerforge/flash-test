from .plugins.brick_imu_v2 import Plugin as brick_imu_v2_class
from .plugins.brick_master import Plugin as brick_master_class
from .plugins.bricklet_accelerometer import Plugin as bricklet_accelerometer_class
from .plugins.bricklet_ambient_light_v2 import Plugin as bricklet_ambient_light_v2_class
from .plugins.bricklet_analog_in_v2 import Plugin as bricklet_analog_in_v2_class
from .plugins.bricklet_analog_out_v2 import Plugin as bricklet_analog_out_v2_class
from .plugins.bricklet_barometer import Plugin as bricklet_barometer_class
from .plugins.bricklet_dual_button import Plugin as bricklet_dual_button_class
from .plugins.bricklet_dust_detector import Plugin as bricklet_dust_detector_class
from .plugins.bricklet_industrial_analog_out import Plugin as bricklet_industrial_analog_out_class
from .plugins.bricklet_industrial_digital_in_4 import Plugin as bricklet_industrial_digital_in_4_class
from .plugins.bricklet_industrial_dual_analog_in import Plugin as bricklet_industrial_dual_analog_in_class
from .plugins.bricklet_laser_range_finder import Plugin as bricklet_laser_range_finder_class
from .plugins.bricklet_lcd_20x4 import Plugin as bricklet_lcd_20x4_class
from .plugins.bricklet_load_cell import Plugin as bricklet_load_cell_class
from .plugins.bricklet_moisture import Plugin as bricklet_moisture_class
from .plugins.bricklet_remote_switch import Plugin as bricklet_remote_switch_class
from .plugins.bricklet_rs232 import Plugin as bricklet_rs232_class
from .plugins.bricklet_sound_intensity import Plugin as bricklet_sound_intensity_class

device_classes = [
    brick_imu_v2_class,
    brick_master_class,
    bricklet_accelerometer_class,
    bricklet_ambient_light_v2_class,
    bricklet_analog_in_v2_class,
    bricklet_analog_out_v2_class,
    bricklet_barometer_class,
    bricklet_dual_button_class,
    bricklet_dust_detector_class,
    bricklet_industrial_analog_out_class,
    bricklet_industrial_digital_in_4_class,
    bricklet_industrial_dual_analog_in_class,
    bricklet_laser_range_finder_class,
    bricklet_lcd_20x4_class,
    bricklet_load_cell_class,
    bricklet_moisture_class,
    bricklet_remote_switch_class,
    bricklet_rs232_class,
    bricklet_sound_intensity_class,
]
