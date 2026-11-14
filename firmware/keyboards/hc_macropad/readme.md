# HC-Macropad

15-key, two-encoder macropad by kikiisacat, using a Seeed Studio XIAO RP2040,
MCP23017 matrix expander, 16 SK6812MINI-E LEDs and an optional 128x32 SSD1306 OLED.

* Hardware: https://github.com/kikiisacat/HC-Macropad
* Maintainer: [kikiisacat](https://github.com/kikiisacat)
* Bootloader: hold the XIAO BOOT button while connecting USB, or double-tap RESET after installing QMK.

Build with `qmk compile -kb hc_macropad -km default` after copying this folder
to `qmk_firmware/keyboards/hc_macropad`.

Full wiring, key assignments and flashing instructions are in the hardware
repository's [firmware guide](https://github.com/kikiisacat/HC-Macropad/blob/main/firmware/README.md).
