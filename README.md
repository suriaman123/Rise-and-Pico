# Rise-and-Pico
A Raspberry Pi Pico W project that wakes you up with sound when it senses daylight. `inspired by Süße Träume`

## How it works
- An LDR (light sensor) near the window feeds a voltage divider into GPIO26 (ADC).
- When the reading crosses a brightness threshold, the alarm starts.
- A DFPlayer Mini plays a random "wake up" track from a small set, with volume ramping up over time.
- A button (GPIO7) can stop the alarm early.
- The alarm re-arms itself only after it's been dark again for a while, so it won't keep re-triggering.

## Hardware
- Raspberry Pi Pico W
- DFPlayer Mini
- Speaker
- LDR (GL5528) + 10k ohm resistor (voltage divider)
- LED
- Push button 
- 1k ohm resistor 

## Setup
1. Load `0001.mp3`, `0002.mp3`, `0003.mp3` (or more) onto the DFPlayer's SD card.
2. Flash `main.py` to the Pico W.
3. Calibrate `light_threshold` in the script by checking ADC readings at your window during the day vs night.
4. Place it near the window before sleeping.
5. Keep it in a dark place during the day.

## Next iteration
In the next iteration, I will add a battery, an on/off switch, and an initial delay, as currently it goes off right from the get-go.😅


### Alternate Project Names
- Rise & Pico
- WakeMate
- Morning Buddy
- PicoAlarm
