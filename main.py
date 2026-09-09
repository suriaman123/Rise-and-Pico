"""
Rise&Pico - Light-Triggered Wake-Up Alarm
Raspberry Pi Pico W + DFPlayer Mini + LDR

"""

from machine import Pin, ADC, UART
import time
import random


light_threshold = 30000          # ADC raw value (0-65535). Tune this by testing at your window.
volume_min = 6                   # DFPlayer volume 
volume_max = 30
volume_increase_interval = 10     # seconds between volume increases
rearm_time = 300                 # 5 minutes
sound = [1, 2, 3]                # 0001.mp3, 0002.mp3, 0003.mp3 on the SD card 


ldr = ADC(Pin(26))
button = Pin(7, Pin.IN, Pin.PULL_UP)   # pressed = LOW
led = Pin(15, Pin.OUT)                

# DFPlayer
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

#DFPlayer command
def df_send(cmd, param1=0, param2=0):
    packet = bytearray([0x7E, 0xFF, 0x06, cmd, 0x00, param1, param2, 0x00, 0x00, 0xEF])
    checksum = 0 - sum(packet[1:7])
    packet[7] = (checksum >> 8) & 0xFF
    packet[8] = checksum & 0xFF
    uart.write(packet)

def df_set_volume(vol):
    vol = max(0, min(30, vol))      # protects the DFPlayer from invalid volume values
    df_send(0x06, 0x00, vol)

def df_play_track(track):
    df_send(0x03, 0x00, track)

def df_stop():
    df_send(0x16, 0x00, 0x00)


alarm_active = False
armed = True            #  alarm is ready to start when it becomes bright
dark_since = None

def read_light():
    return ldr.read_u16()

def button_pressed():
    return button.value() == 0

def start_alarm():
    global alarm_active
    alarm_active = True
    led.value(1)
    df_set_volume(volume_min)
    track = random.choice(sound)
    df_play_track(track)
    print("Alarm started, track:", track)

def stop_alarm():
    global alarm_active, armed
    alarm_active = False
    armed = False
    led.value(0)
    df_stop()
    print("Alarm stopped")


def main():
    global armed, dark_since
    current_volume = volume_min
    last_time_volume_increased = time.time()

    print("Alarm system ready. Threshold =", light_threshold)

    while True:
        light = read_light()
        is_bright = light > light_threshold

        # Track how long it's been dark, to re-arm the alarm after 5 minutes
        if not is_bright:
            if dark_since is None:
                dark_since = time.time()
            elif not armed and (time.time() - dark_since) > rearm_time:
                armed = True
                print("Re-armed after darkness")
        else:
            dark_since = None

        if alarm_active:
            # Check for button press 
            if button_pressed():
                stop_alarm()
            else:
                # Increase volume up over time
                now = time.time()
                if now - last_time_volume_increased >= volume_increase_interval and current_volume < volume_max:
                    current_volume += 2     # increase volume by two
                    df_set_volume(current_volume)
                    last_time_volume_increased = now
                    print("Volume ->", current_volume)
        else:
            if is_bright and armed:
                current_volume = volume_min
                last_time_volume_increased = time.time()
                start_alarm()

        time.sleep(1)

main()
