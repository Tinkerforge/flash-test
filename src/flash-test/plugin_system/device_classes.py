from .plugins.brick_dc import Plugin as brick_dc_class
from .plugins.brick_imu_v2 import Plugin as brick_imu_v2_class
from .plugins.brick_master import Plugin as brick_master_class
from .plugins.brick_servo import Plugin as brick_servo_class
from .plugins.brick_stepper import Plugin as brick_stepper_class
from .plugins.bricklet_accelerometer import Plugin as bricklet_accelerometer_class
from .plugins.bricklet_ambient_light_v2 import Plugin as bricklet_ambient_light_v2_class
from .plugins.bricklet_analog_in_v2 import Plugin as bricklet_analog_in_v2_class
from .plugins.bricklet_analog_out_v2 import Plugin as bricklet_analog_out_v2_class
from .plugins.bricklet_barometer import Plugin as bricklet_barometer_class
from .plugins.bricklet_co2 import Plugin as bricklet_co2_class
from .plugins.bricklet_color import Plugin as bricklet_color_class
from .plugins.bricklet_distance_ir import Plugin as bricklet_distance_ir_class
from .plugins.bricklet_dual_button import Plugin as bricklet_dual_button_class
from .plugins.bricklet_dual_relay import Plugin as bricklet_dual_relay_class
from .plugins.bricklet_dust_detector import Plugin as bricklet_dust_detector_class
from .plugins.bricklet_humidity import Plugin as bricklet_humidity_class
from .plugins.bricklet_industrial_analog_out import Plugin as bricklet_industrial_analog_out_class
from .plugins.bricklet_industrial_digital_in_4 import Plugin as bricklet_industrial_digital_in_4_class
from .plugins.bricklet_industrial_dual_analog_in import Plugin as bricklet_industrial_dual_analog_in_class
from .plugins.bricklet_io16 import Plugin as bricklet_io16_class
from .plugins.bricklet_joystick import Plugin as bricklet_joystick_class
from .plugins.bricklet_laser_range_finder import Plugin as bricklet_laser_range_finder_class
from .plugins.bricklet_lcd_20x4 import Plugin as bricklet_lcd_20x4_class
from .plugins.bricklet_led_strip import Plugin as bricklet_led_strip_class
from .plugins.bricklet_load_cell import Plugin as bricklet_load_cell_class
from .plugins.bricklet_moisture import Plugin as bricklet_moisture_class
from .plugins.bricklet_motion_detector import Plugin as bricklet_motion_detector_class
from .plugins.bricklet_oled_128x64 import Plugin as bricklet_oled_128x64_class
from .plugins.bricklet_oled_64x48 import Plugin as bricklet_oled_64x48_class
from .plugins.bricklet_ptc import Plugin as bricklet_ptc_class
from .plugins.bricklet_real_time_clock import Plugin as bricklet_real_time_clock_class
from .plugins.bricklet_remote_switch import Plugin as bricklet_remote_switch_class
from .plugins.bricklet_rotary_encoder import Plugin as bricklet_rotary_encoder_class
from .plugins.bricklet_rotary_poti import Plugin as bricklet_rotary_poti_class
from .plugins.bricklet_rs232 import Plugin as bricklet_rs232_class
from .plugins.bricklet_segment_display_4x7 import Plugin as bricklet_segment_display_4x7_class
from .plugins.bricklet_solid_state_relay import Plugin as bricklet_solid_state_relay_class
from .plugins.bricklet_sound_intensity import Plugin as bricklet_sound_intensity_class
from .plugins.bricklet_temperature import Plugin as bricklet_temperature_class
from .plugins.bricklet_temperature_ir import Plugin as bricklet_temperature_ir_class
from .plugins.bricklet_thermocouple import Plugin as bricklet_thermocouple_class
from .plugins.bricklet_uv_light import Plugin as bricklet_uv_light_class
from .plugins.bricklet_voltage_current import Plugin as bricklet_voltage_current_class
from .plugins.extension_ethernet import Plugin as extension_ethernet_class
from .plugins.extension_rs485 import Plugin as extension_rs485_class

device_classes = [
    brick_dc_class,
    brick_imu_v2_class,
    brick_master_class,
    brick_servo_class,
    brick_stepper_class,
    bricklet_accelerometer_class,
    bricklet_ambient_light_v2_class,
    bricklet_analog_in_v2_class,
    bricklet_analog_out_v2_class,
    bricklet_barometer_class,
    bricklet_co2_class,
    bricklet_color_class,
    bricklet_distance_ir_class,
    bricklet_dual_button_class,
    bricklet_dual_relay_class,
    bricklet_dust_detector_class,
    bricklet_humidity_class,
    bricklet_industrial_analog_out_class,
    bricklet_industrial_digital_in_4_class,
    bricklet_industrial_dual_analog_in_class,
    bricklet_io16_class,
    bricklet_joystick_class,
    bricklet_laser_range_finder_class,
    bricklet_lcd_20x4_class,
    bricklet_led_strip_class,
    bricklet_load_cell_class,
    bricklet_moisture_class,
    bricklet_motion_detector_class,
    bricklet_oled_128x64_class,
    bricklet_oled_64x48_class,
    bricklet_ptc_class,
    bricklet_real_time_clock_class,
    bricklet_remote_switch_class,
    bricklet_rotary_encoder_class,
    bricklet_rotary_poti_class,
    bricklet_rs232_class,
    bricklet_segment_display_4x7_class,
    bricklet_solid_state_relay_class,
    bricklet_sound_intensity_class,
    bricklet_temperature_class,
    bricklet_temperature_ir_class,
    bricklet_thermocouple_class,
    bricklet_uv_light_class,
    bricklet_voltage_current_class,
    extension_ethernet_class,
    extension_rs485_class,
]
