# ESP32 Smart Auto / Manual Lighting System

## Projektbeschreibung (Deutsch)

Dieses Projekt demonstriert ein intelligentes adaptives Beleuchtungssystem mit ESP32, LDR-Lichtsensor, PIR-Bewegungssensor, PWM-Technologie und manueller Steuerung.

Das System analysiert kontinuierlich die Umgebungshelligkeit und erkennt Bewegungen in Echtzeit.

### Systemverhalten

- Bei heller Umgebung bleiben die LEDs ausgeschaltet.
- Bei Dunkelheit aktiviert das System automatisch die Beleuchtung.
- Wenn eine Bewegung erkannt wird, wechseln die LEDs sanft zur maximalen Helligkeit.
- Nach Ablauf des Timers dimmen die LEDs automatisch zurück in den Energiesparmodus.
- Die LEDs verwenden PWM-Fade-In und Fade-Out für weiche Übergänge.
- Ein Push-Button ermöglicht den Wechsel zwischen:
  - AUTO MODE
  - MANUAL ON
  - MANUAL OFF

---

# Verwendete Komponenten

| Komponente | Beschreibung |
|---|---|
| ESP32 | Hauptcontroller |
| LDR Sensor | Misst die Lichtintensität |
| PIR Motion Sensor | Erkennt Bewegungen |
| LEDs | Beleuchtungsausgabe |
| Push Button | Umschalten der Betriebsmodi |
| Breadboard & Jumper | Verbindung der Komponenten |

---

# Betriebsmodi

| Modus | Funktion |
|---|---|
| AUTO MODE | Intelligente automatische Steuerung |
| MANUAL ON | LEDs dauerhaft eingeschaltet |
| MANUAL OFF | LEDs dauerhaft ausgeschaltet |

---

# Systemlogik

- Helle Umgebung → LEDs AUS
- Dunkle Umgebung ohne Bewegung → LEDs stark gedimmt
- Dunkle Umgebung mit Bewegung → LEDs maximale Helligkeit
- Nach Bewegung → LEDs bleiben einige Sekunden hell
- Danach → LEDs dimmen automatisch zurück

---

# Vorteile des Projekts

Dieses intelligente Beleuchtungssystem kann verwendet werden in:

- Smart Homes
- Intelligenter Straßenbeleuchtung
- Solarbeleuchtungssystemen
- Garagen
- Sicherheitsanlagen
- Lagerräumen
- Energieeffizienten Gebäuden
- Smart Energy Anwendungen
- IoT Automatisierungssystemen

Das Projekt zeigt, wie intelligente IoT-Systeme den Energieverbrauch reduzieren können, indem Beleuchtung nur bei Bedarf aktiviert wird.

---

# MicroPython Code

```python
from machine import Pin, ADC, PWM
import time

leds = PWM(Pin(14))
leds.freq(1000)

internal_led = Pin(2, Pin.OUT)

light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)
light_sensor.width(ADC.WIDTH_12BIT)

motion_sensor = Pin(27, Pin.IN)

button = Pin(25, Pin.IN, Pin.PULL_UP)

motion_timeout = 5
last_motion_time = 0

current_brightness = 0

mode = 0
last_button_state = 1

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

print("Smart Auto / Manual Lighting System Running...")

while True:

    button_state = button.value()

    if button_state == 0 and last_button_state == 1:

        mode += 1

        if mode > 2:
            mode = 0

        time.sleep(0.3)

    last_button_state = button_state

    if mode == 0:

        light_value = light_sensor.read()
        motion = motion_sensor.value()

        if light_value < 1800:

            fade_to(0)
            internal_led.off()

        else:

            if motion == 1:

                last_motion_time = time.time()

                fade_to(1023)
                internal_led.on()

            else:

                elapsed = time.time() - last_motion_time

                if elapsed < motion_timeout:

                    fade_to(1023)
                    internal_led.on()

                else:

                    fade_to(50)
                    internal_led.on()

    elif mode == 1:

        fade_to(1023)
        internal_led.on()

    elif mode == 2:

        fade_to(0)
        internal_led.off()

    time.sleep(0.2)
```

---

# ESP32 Smart Auto / Manual Lighting System

## Project Description (English)

This project demonstrates an intelligent adaptive lighting system using ESP32, an LDR light sensor, a PIR motion sensor, PWM technology, and manual control.

The system continuously analyzes ambient light intensity and detects movement in real time.

### System Behavior

- In bright environments, the LEDs remain OFF.
- In dark environments, the system automatically activates the lighting.
- When motion is detected, the LEDs smoothly fade to maximum brightness.
- After the timeout period, the LEDs automatically dim back to energy-saving mode.
- PWM fade-in and fade-out effects provide smooth lighting transitions.
- A push button allows switching between:
  - AUTO MODE
  - MANUAL ON
  - MANUAL OFF

---

# Components Used

| Component | Description |
|---|---|
| ESP32 | Main microcontroller |
| LDR Sensor | Measures ambient light intensity |
| PIR Motion Sensor | Detects movement |
| LEDs | Lighting output |
| Push Button | Changes operating modes |
| Breadboard & Jumper Wires | Circuit connections |

---

# Operating Modes

| Mode | Function |
|---|---|
| AUTO MODE | Intelligent automatic control |
| MANUAL ON | LEDs permanently ON |
| MANUAL OFF | LEDs permanently OFF |

---

# System Logic

- Bright environment → LEDs OFF
- Dark environment without motion → LEDs dimmed
- Dark environment with motion → LEDs maximum brightness
- After motion → LEDs stay bright for a few seconds
- Then → LEDs automatically dim back

---

# Project Benefits

This intelligent lighting system can be used in:

- Smart homes
- Smart street lighting
- Solar lighting systems
- Garages
- Security systems
- Warehouses
- Energy-efficient buildings
- Smart energy applications
- IoT automation systems

The project demonstrates how intelligent IoT systems can reduce energy consumption by activating lighting only when required.

---

# MicroPython Code

```python
from machine import Pin, ADC, PWM
import time

leds = PWM(Pin(14))
leds.freq(1000)

internal_led = Pin(2, Pin.OUT)

light_sensor = ADC(Pin(34))
light_sensor.atten(ADC.ATTN_11DB)
light_sensor.width(ADC.WIDTH_12BIT)

motion_sensor = Pin(27, Pin.IN)

button = Pin(25, Pin.IN, Pin.PULL_UP)

motion_timeout = 5
last_motion_time = 0

current_brightness = 0

mode = 0
last_button_state = 1

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

print("Smart Auto / Manual Lighting System Running...")

while True:

    button_state = button.value()

    if button_state == 0 and last_button_state == 1:

        mode += 1

        if mode > 2:
            mode = 0

        time.sleep(0.3)

    last_button_state = button_state

    if mode == 0:

        light_value = light_sensor.read()
        motion = motion_sensor.value()

        if light_value < 1800:

            fade_to(0)
            internal_led.off()

        else:

            if motion == 1:

                last_motion_time = time.time()

                fade_to(1023)
                internal_led.on()

            else:

                elapsed = time.time() - last_motion_time

                if elapsed < motion_timeout:

                    fade_to(1023)
                    internal_led.on()

                else:

                    fade_to(50)
                    internal_led.on()

    elif mode == 1:

        fade_to(1023)
        internal_led.on()

    elif mode == 2:

        fade_to(0)
        internal_led.off()

    time.sleep(0.2)
```

---

## Developer

**Ahmad Azroun**  
Renewable Energy Manager | IoT & Smart Energy Systems Developer
