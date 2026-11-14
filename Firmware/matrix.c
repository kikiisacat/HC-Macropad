#include "matrix.h"
#include "i2c_master.h"
#include "timer.h"
#include "wait.h"
// A0/A1/A2 grounded
#define MCP_ADDRESS (0x20 << 1)
#define MCP_TIMEOUT 2
#define MCP_RETRY_MS 100
#define IODIRA 0x00
#define IPOLA  0x02
#define GPPUA  0x0C
#define GPIOA  0x12
#define GPIOB  0x13
#define OLATA  0x14

static bool connected;
static uint16_t retry_at;

bool hc_matrix_connected(void) {
    return connected;
}

static bool write_reg(uint8_t reg, uint8_t value) {
    return i2c_write_register(MCP_ADDRESS, reg, &value, 1, MCP_TIMEOUT) == I2C_STATUS_SUCCESS;
}

static bool configure_expander(void) {
    const uint8_t directions[] = {0x07, 0xFF};
    const uint8_t polarity[] = {0, 0};
    const uint8_t pullups[] = {0x07, 0x03};
    return write_reg(OLATA, 0xF8) &&
           i2c_write_register(MCP_ADDRESS, IPOLA, polarity, 2, MCP_TIMEOUT) == I2C_STATUS_SUCCESS &&
           i2c_write_register(MCP_ADDRESS, GPPUA, pullups, 2, MCP_TIMEOUT) == I2C_STATUS_SUCCESS &&
           i2c_write_register(MCP_ADDRESS, IODIRA, directions, 2, MCP_TIMEOUT) == I2C_STATUS_SUCCESS;
}

void matrix_init_custom(void) {
    i2c_init();
    connected = configure_expander();
    retry_at = timer_read();
}

bool matrix_scan_custom(matrix_row_t current_matrix[]) {
    matrix_row_t next[MATRIX_ROWS] = {0};
    if (!connected && timer_elapsed(retry_at) >= MCP_RETRY_MS) {
        connected = configure_expander();
        retry_at = timer_read();
    }

    if (connected) {
        bool ok = true;
        for (uint8_t row = 0; row < 5; row++) {
            const uint8_t drive = 0xF8 & ~(1U << (row + 3));
            uint8_t inputs = 0xFF;
            if (!write_reg(OLATA, drive)) {
                ok = false;
                break;
            }
            wait_us(30);
            if (i2c_read_register(MCP_ADDRESS, GPIOA, &inputs, 1, MCP_TIMEOUT) != I2C_STATUS_SUCCESS) {
                ok = false;
                break;
            }
            next[row] = ~inputs & 0x07;
        }
        if (!write_reg(OLATA, 0xF8)) ok = false;
        uint8_t buttons = 0xFF;
        if (ok && i2c_read_register(MCP_ADDRESS, GPIOB, &buttons, 1, MCP_TIMEOUT) != I2C_STATUS_SUCCESS) ok = false;
        if (ok) {
            next[5] = ~buttons & 0x03;
        } else {
            for (uint8_t row = 0; row < MATRIX_ROWS; row++) next[row] = 0;
            connected = false;
            retry_at = timer_read();
        }
    }
    bool changed = false;
    for (uint8_t row = 0; row < MATRIX_ROWS; row++) {
        if (current_matrix[row] != next[row]) {
            current_matrix[row] = next[row];
            changed = true;
        }
    }
    return changed;
}
