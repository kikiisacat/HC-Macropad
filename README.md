# HC-Macropad
A custom 15-key/2-dial/oled macropad. It will be put to good use to open programs, run complex commands, and execute multi-step actions.
I plan to purchase all parts marked with a "0" in the BOM out of pocket.
# Why I made it
I wanted to learn PCB design basics. I also wanted many custom keys for productivity, and chose this 2-dial and 15-key layout for this reason. I chose to use a MCP23017 to get access to more than 8 inputs.
# Parts
Seeed Studio Xiao RP2040
15 Switches
2 EC11E Rotary Encoders that also act as buttons
0.91 in OLED
16 SK6812 MINI-E RGB LEDs, 15 for keys, 1 for status/additional
MCP23017 for more inputs
74AHCT125 for LED buffer \
Keycap files were from here: https://github.com/anhthang/dsa-keycap

# Use
Install the [QMK firmware](firmware/README.md), then assign the F13–F24 keys to the shortcuts. The firmware includes both dials, their push buttons, RGB lighting, and OLED.

# Images
<img width="3172" height="871" alt="image" src="https://github.com/user-attachments/assets/5e939bea-3aad-41b5-9287-4bee6e5e041c" />

<img width="1120" height="917" alt="image" src="https://github.com/user-attachments/assets/f1f1f926-3fab-4002-b022-143afbc58d03" />

<img width="752" height="781" alt="image" src="https://github.com/user-attachments/assets/2ac7bad0-5bd3-44c3-a760-32831c46c6c5" />

<img width="1174" height="850" alt="image" src="https://github.com/user-attachments/assets/509faf6c-1588-4a51-a4ab-4917d19df9c0" />
