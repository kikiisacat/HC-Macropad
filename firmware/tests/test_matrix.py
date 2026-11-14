#!/usr/bin/env python3
"""Compile and exercise the real scanner against an emulated MCP23017."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
headers = {
    'matrix.h': '#include <stdint.h>\n#include <stdbool.h>\n#define MATRIX_ROWS 6\n#define MATRIX_COLS 3\ntypedef uint8_t matrix_row_t;\n',
    'i2c_master.h': '#include <stdint.h>\ntypedef int16_t i2c_status_t;\n#define I2C_STATUS_SUCCESS 0\nvoid i2c_init(void);\ni2c_status_t i2c_write_register(uint8_t,uint8_t,const uint8_t*,uint16_t,uint16_t);\ni2c_status_t i2c_read_register(uint8_t,uint8_t,uint8_t*,uint16_t,uint16_t);\n',
    'timer.h': '#include <stdint.h>\nuint16_t timer_read(void);\nuint16_t timer_elapsed(uint16_t);\n',
    'wait.h': '#include <stdint.h>\nvoid wait_us(uint16_t);\n',
}
harness = r'''
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "SCANNER"
static uint8_t regs[0x16], held[5], push;
static uint16_t now;
static int calls, fail_at;
void i2c_init(void) {}
uint16_t timer_read(void) {return now;}
uint16_t timer_elapsed(uint16_t start) {return (uint16_t)(now-start);}
void wait_us(uint16_t us) {assert(us >= 1);}
static bool fails(void) {return ++calls == fail_at;}
i2c_status_t i2c_write_register(uint8_t addr,uint8_t reg,const uint8_t *data,uint16_t len,uint16_t timeout) {
    assert(addr==0x40 && timeout==2 && reg+len<=sizeof(regs));
    if(fails()) return -2;
    memcpy(regs+reg,data,len);
    return 0;
}
i2c_status_t i2c_read_register(uint8_t addr,uint8_t reg,uint8_t *data,uint16_t len,uint16_t timeout) {
    assert(addr==0x40 && timeout==2 && len==1);
    *data=0; // Failed reads must never become phantom presses.
    if(fails()) return -2;
    assert(reg==0x12 || reg==0x13);
    *data=0xFF;
    if(reg==0x13) *data &= ~push;
    else for(int r=0;r<5;r++) if(!(regs[0x14]&(1<<(r+3)))) *data &= ~held[r];
    return 0;
}
static void reset(void) {
    memset(regs,0,sizeof(regs)); memset(held,0,sizeof(held));
    push=0; calls=0; fail_at=0; now=0; matrix_init_custom();
    assert(hc_matrix_connected());
    assert(regs[0]==7 && regs[1]==255 && regs[0x0C]==7 && regs[0x0D]==3 && regs[0x14]==0xF8);
}
static void released(matrix_row_t *m) {for(int r=0;r<6;r++) assert(m[r]==0);}
int main(void) {
    matrix_row_t m[6]={0}; reset();
    assert(!matrix_scan_custom(m));
    for(int r=0;r<5;r++) for(int c=0;c<3;c++) {
        held[r]=1<<c; assert(matrix_scan_custom(m));
        for(int i=0;i<6;i++) assert(m[i]==(i==r?(1<<c):0));
        held[r]=0; assert(matrix_scan_custom(m)); released(m);
    }
    for(int b=0;b<2;b++) {
        push=1<<b; assert(matrix_scan_custom(m)); assert(m[5]==push);
        push=0; assert(matrix_scan_custom(m)); released(m);
    }
    for(int r=0;r<5;r++) held[r]=7;
    push=3; assert(matrix_scan_custom(m));
    for(int r=0;r<5;r++) assert(m[r]==7);
    assert(m[5]==3 && regs[0x14]==0xF8);
    assert(!matrix_scan_custom(m));
    // Fail each transaction in a scan: all keys release, then recover.
    for(int op=1;op<=12;op++) {
        reset(); held[0]=3; push=3; matrix_scan_custom(m);
        fail_at=calls+op;
        assert(matrix_scan_custom(m)); released(m); assert(!hc_matrix_connected());
        fail_at=0; now=99; assert(!matrix_scan_custom(m)); released(m);
        now=100; assert(matrix_scan_custom(m)); assert(hc_matrix_connected());
        assert(m[0]==3 && m[5]==3);
    }
    // Every possible configuration failure must also retry without phantom keys.
    for(int op=1;op<=4;op++) {
        reset(); calls=0; fail_at=op; matrix_init_custom();
        assert(!hc_matrix_connected()); matrix_scan_custom(m); released(m);
        now=100; fail_at=0; matrix_scan_custom(m); assert(hc_matrix_connected());
    }
    // Retry interval remains correct across the 16-bit timer wrap.
    reset(); now=65500; fail_at=calls+1; matrix_scan_custom(m);
    fail_at=0; now=63; matrix_scan_custom(m); assert(!hc_matrix_connected());
    now=64; matrix_scan_custom(m); assert(hc_matrix_connected());
    puts("PASS: 15 keys, 2 buttons, simultaneous presses, all scan/config failures, reconnect, timer wrap");
}
'''
with tempfile.TemporaryDirectory() as directory:
    p = Path(directory)
    for name, content in headers.items():
        (p / name).write_text(content)
    scanner = root / 'keyboards/hc_macropad/matrix.c'
    (p / 'test.c').write_text(harness.replace('SCANNER', str(scanner)))
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-I', str(p), str(p/'test.c'), '-o', str(p/'test')], check=True)
    subprocess.run([str(p/'test')], check=True)
