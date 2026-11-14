#!/usr/bin/env python3
"""Check the QMK layout against a KiCad XML netlist exported from this PCB."""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parents[1]
netlist = ET.parse(sys.argv[1]).getroot()
pins = {}
for net in netlist.findall('./nets/net'):
    for node in net.findall('node'):
        pins[node.get('ref'), node.get('pin')] = net.get('name')
layout = json.loads((root/'keyboards/hc_macropad/keyboard.json').read_text())['layouts']['LAYOUT']['layout']
by_name = {key['label']: key for key in layout}
for i in range(1,16):
    col = int(pins[f'SW{i}', '1'].removeprefix('/GPA'))
    assert pins[f'SW{i}','2'] == pins[f'D{i}','2']
    row = int(pins[f'D{i}','1'].removeprefix('/GPA')) - 3
    assert by_name[f'SW{i}']['matrix'] == [row,col]
    assert [by_name[f'SW{i}']['x'],by_name[f'SW{i}']['y']] == [(i-1)//3,(i-1)%3+1]
for i in range(2):
    ref=f'SW{16+i}'
    assert pins[ref,'S1'] == f'/GPB{i}'
    assert pins[ref,'S2'] == pins[ref,'C'] == '/GND'
    assert pins[ref,'A'] == f'/D{2*i}' and pins[ref,'B'] == f'/D{2*i+1}'
    assert by_name[f'{ref} push']['matrix'] == [5,i]
for pin,net in [('5','/SDA'),('6','/SCL'),('7','/D6')]: assert pins['U1',pin]==net
for pin in ['15','16','17']: assert pins['U2',pin]=='/GND'
assert pins['U2','9']=='/3.3V'
assert pins['U3','2']=='/D6'
assert pins['U3','3']==pins['R4','2']
assert pins['D17','2']==pins['R4','1']
for i in range(17,32): assert pins[f'D{i}','4']==pins[f'D{i+1}','2']
assert len([c for c in netlist.findall('./components/comp') if c.findtext('value')=='SK6812MINI-E'])==16
print('PASS: schematic matrix, encoder signals/buttons, I2C, expander address/power, 16-LED chain match firmware')
