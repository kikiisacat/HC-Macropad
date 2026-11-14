# QMK firmware

Firmware for the HC-Macropad's **Seeed Studio XIAO RP2040**. The build includes
15 keys, both encoder buttons, two rotary encoders, 16 SK6812MINI-E RGB LEDs
and a 128x32 SSD1306 I²C OLED. Use the RP2040 XIAO; the SAMD21 XIAO needs different
firmware. The original schematic symbol still contains SAMD21 port names, so
the configuration follows the physical XIAO D0–D6 pads and RP2040 pinout instead.

## Install

1. Download [`hc_macropad_default.uf2`](dist/hc_macropad_default.uf2).
2. Hold the XIAO's **BOOT** button while connecting a USB data cable.
3. Copy the UF2 to the **RPI-RP2** drive that appears. The drive will disconnect
   and the board will restart as **HC-Macropad**.
4. Test every key and both dials. No application is needed for the media keys.
   Assign the F13–F24 keys to actions in your operating system or macro software.

Once QMK is installed, double-tap RESET to return to the bootloader. You can
also hold the bottom-right key and tap the key immediately to its left.
The build script only compiles; it does not flash connected hardware.

## Default controls

Physical layout, with USB and the dials at the top:

| | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|---|---|---|---|---|---|
| Top | F13 (SW1) | F14 (SW4) | F15 (SW7) | F16 (SW10) | F17 (SW13) |
| Middle | F18 (SW2) | F19 (SW5) | F20 (SW8) | F21 (SW11) | F22 (SW14) |
| Bottom | F23 (SW3) | F24 (SW6) | Previous track (SW9) | Next track (SW12) | Hold for lighting (SW15) |

* Left dial (SW16): volume; press to mute.
* Right dial (SW17): vertical scrolling; press to play/pause.
* While holding SW15: left dial changes hue; right dial changes brightness.

Lighting-layer keys:

| | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 |
|---|---|---|---|---|---|
| Top | RGB on/off | Next effect | Previous effect | Hue up | Hue down |
| Middle | Saturation up | Saturation down | Brightness up | Brightness down | Unassigned |
| Bottom | Unassigned | Unassigned | Unassigned | Enter bootloader | Hold lighting |

The RGB default is cyan at brightness 32/255, capped at 64/255. Static color,
breathing and rainbow effects are included. The onboard XIAO LED is separate
from the 16 PCB LEDs and is not controlled by these effects.

## Wiring used by this build

| Signal | Connection |
|---|---|
| SW16 encoder A / B | XIAO D0 / D1 → GP26 / GP27 |
| SW17 encoder A / B | XIAO D2 / D3 → GP28 / GP29 |
| SDA / SCL | XIAO D4 / D5 → GP6 / GP7, hardware I2C1 at 400 kHz |
| LED data | XIAO D6 → GP0 → 74AHCT125 → R4 → D17–D32 |
| MCP23017 | Address 0x20, A0/A1/A2 grounded, powered at 3.3 V |
| Key matrix inputs | GPA0–GPA2, internal pull-ups enabled |
| Key matrix scan outputs | GPA3–GPA7, one driven low at a time |
| SW16 / SW17 buttons | GPB0 / GPB1, active low with pull-ups |
| OLED J1 pads 1–4 | SDA, SCL, 3.3 V, GND |

The electrical matrix is five rows by three columns. Its physical layout is
three rows by five columns; `keyboard.json` maps between them. A sixth logical
row holds the two encoder buttons. The unused cell is disabled. Normal QMK
debouncing is applied to all 17 switches.

The scanner releases keys on any failed I²C scan, discards partial reads and
retries the expander configuration every 100 ms. Encoder rotation is read
directly from the RP2040 pins. It does not go through the expander.

The OLED assumes an SSD1306 **128x32 at 0x3C**. Confirm your module's pin order
against J1 before connecting it. An absent OLED does not prevent the key matrix
from starting. Change the OLED defines in `config.h` for a different supported
display. Encoder resolution defaults to **2 transitions per action**, common
for EC11 encoders with two detents per quadrature cycle. If a particular encoder
skips detents or reports twice per detent, adjust its `resolution` in
`keyboard.json` to match the hardware. Swap that encoder's `pin_a` and `pin_b`
if clockwise turns act in the opposite direction.

## Change mappings and rebuild

Edit [`keymaps/default/keymap.c`](keyboards/hc_macropad/keymaps/default/keymap.c)
for keys and encoder actions. This build uses QMK source keymaps; it does not
include VIA support. Opening applications and running commands requires
host-side bindings; firmware sends the assigned keycodes.

Install the [QMK development environment](https://docs.qmk.fm/newbs_getting_started)
and its ARM toolchain, then run from this repository:

```sh
bash firmware/build.sh /path/to/qmk_firmware
```

The script copies this keyboard definition into the supplied QMK checkout and
places the compiled UF2 in `firmware/dist`. It replaces an existing
`keyboards/hc_macropad` definition in that checkout.

The distributed UF2 was built with **QMK 0.34.7**, commit
`180f394b489c238cb231c2bf8b080262155e03c0`, using QMK's ARM GCC **15.2.0**.
Firmware source is GPL-2.0-or-later; see [`LICENSE`](LICENSE). The repository's
root license continues to cover its other content.

## Validation

Run the scanner tests with a host C compiler:

```sh
python3 firmware/tests/test_matrix.py
```

They exercise all 15 keys, both encoder buttons, simultaneous presses,
every I²C transaction failure point, initialization failures, reconnects
and timer wraparound against an emulated MCP23017.

Check the layout against the current schematic:

```sh
kicad-cli sch export netlist --format kicadxml -o /tmp/macropad.xml PCB/Macropad.kicad_sch
python3 firmware/tests/check_wiring.py /tmp/macropad.xml
```

Compilation and software tests pass. The UF2 has **not been flashed or tested
on assembled hardware**. First hardware checks are key positions, encoder
direction/resolution, OLED address/orientation, and RGB data/color order.

References: [XIAO RP2040 pin map](https://wiki.seeedstudio.com/XIAO-RP2040/#pin-map),
[QMK custom matrix](https://docs.qmk.fm/custom_matrix),
[QMK RP2040 support](https://docs.qmk.fm/platformdev_rp2040).
