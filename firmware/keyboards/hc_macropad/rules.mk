# SPDX-License-Identifier: GPL-2.0-or-later
CUSTOM_MATRIX = lite
SRC += matrix.c
I2C_DRIVER_REQUIRED = yes
OLED_ENABLE = yes
OLED_DRIVER = ssd1306
OLED_TRANSPORT = i2c
