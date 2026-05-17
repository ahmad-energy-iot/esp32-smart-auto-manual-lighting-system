from machine import Pin, ADC, PWM
import time

# =========================================
# LEDs on GPIO14
# =========================================
leds = PWM(Pin(14))
leds.freq(1000)

# =========================================
# Internal ESP32 Blue LED
# =========================================
internal_led = Pin(2, Pin.OUT)

# =========================================
# Light Sensor on GPIO34
# =========================================
light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)
light_sensor.width(ADC.WIDTH_12BIT)

# =========================================
# PIR Motion Sensor on GPIO27
# =========================================
motion_sensor = Pin(27, Pin.IN)

# =========================================
# Push Button on GPIO25
# =========================================
button = Pin(25, Pin.IN, Pin.PULL_UP)

# =========================================
# Variables
# =========================================
motion_timeout = 5
last_motion_time = 0

current_brightness = 0

# Modes
# 0 = AUTO
# 1 = MANUAL ON
# 2 = MANUAL OFF
mode = 0

last_button_state = 1

# =========================================
# Fade Function
# =========================================
def fade_to(target):

    global current_brightness

    if target > current_brightness:

        for value in range(current_brightness, target + 1, 20):
            leds.duty(value)
            time.sleep(0.05)

    elif target < current_brightness:

        for value in range(current_brightness, target - 1, -20):
            leds.duty(value)
            time.sleep(0.05)

    current_brightness = target
    leds.duty(current_brightness)

# =========================================
# Main Program
# =========================================
print("Smart Auto / Manual Lighting System Running...")

while True:

    # =====================================
    # Button Reading
    # =====================================
    button_state = button.value()

    # Button Press Detection
    if button_state == 0 and last_button_state == 1:

        mode += 1

        if mode > 2:
            mode = 0

        # Print Current Mode
        if mode == 0:
            print("MODE -> AUTO")

        elif mode == 1:
            print("MODE -> MANUAL ON")

        elif mode == 2:
            print("MODE -> MANUAL OFF")

        time.sleep(0.3)

    last_button_state = button_state

    # =====================================
    # AUTO MODE
    # =====================================
    if mode == 0:

        light_value = light_sensor.read()
        motion = motion_sensor.value()

        print("Light:", light_value)
        print("Motion:", motion)

        # Bright Environment
        if light_value < 1800:

            fade_to(0)
            internal_led.off()

            print("Bright Environment -> LEDs OFF")

        # Dark Environment
        else:

            # Motion Detected
            if motion == 1:

                last_motion_time = time.time()

                fade_to(1023)
                internal_led.on()

                print("Motion Detected -> LEDs HIGH")

            else:

                elapsed = time.time() - last_motion_time

                # Keep LEDs bright after motion
                if elapsed < motion_timeout:

                    fade_to(1023)
                    internal_led.on()

                    print("Waiting Timeout -> LEDs STILL HIGH")

                else:

                    fade_to(50)
                    internal_led.on()

                    print("No Motion -> LEDs DIM")

    # =====================================
    # MANUAL ON MODE
    # =====================================
    elif mode == 1:

        fade_to(1023)
        internal_led.on()

        print("MANUAL ON MODE")

    # =====================================
    # MANUAL OFF MODE
    # =====================================
    elif mode == 2:

        fade_to(0)
        internal_led.off()

        print("MANUAL OFF MODE")

    print("---------------------------")

    time.sleep(0.2)