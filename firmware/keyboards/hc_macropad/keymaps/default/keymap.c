// Copyright 2026 kikiisacat
// SPDX-License-Identifier: GPL-2.0-or-later
#include QMK_KEYBOARD_H

enum layers { BASE, LIGHTING };

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [BASE] = LAYOUT(
        KC_F13, KC_F14, KC_F15, KC_F16, KC_F17,
        KC_F18, KC_F19, KC_F20, KC_F21, KC_F22,
        KC_F23, KC_F24, KC_MPRV, KC_MNXT, MO(LIGHTING),
        KC_MUTE, KC_MPLY
    ),
    [LIGHTING] = LAYOUT(
        UG_TOGG, UG_NEXT, UG_PREV, UG_HUEU, UG_HUED,
        UG_SATU, UG_SATD, UG_VALU, UG_VALD, KC_NO,
        KC_NO, KC_NO, KC_NO, QK_BOOT, KC_TRNS,
        KC_TRNS, KC_TRNS
    )
};

const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [BASE] = {ENCODER_CCW_CW(KC_VOLD, KC_VOLU), ENCODER_CCW_CW(MS_WHLD, MS_WHLU)},
    [LIGHTING] = {ENCODER_CCW_CW(UG_HUED, UG_HUEU), ENCODER_CCW_CW(UG_VALD, UG_VALU)}
};

#ifdef OLED_ENABLE
bool oled_task_user(void) {
    oled_write_ln_P(PSTR("HC-Macropad"), false);
    oled_write_ln_P(layer_state_is(LIGHTING) ? PSTR("Layer: Lighting") : PSTR("Layer: Macros  "), false);
    oled_write_ln_P(hc_matrix_connected() ? PSTR("Keys: MCP23017 OK ") : PSTR("Keys: I2C ERROR   "), false);
    oled_write_ln_P(layer_state_is(LIGHTING) ? PSTR("Dial: Hue / Bright   ") : PSTR("Dial: Volume / Scroll"), false);
    return false;
}
#endif
