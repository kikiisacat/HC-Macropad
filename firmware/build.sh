#!/usr/bin/env bash
set -euo pipefail
firmware_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
qmk_home="${1:-${QMK_HOME:-$HOME/qmk_firmware}}"
if [[ ! -f "$qmk_home/quantum/quantum.h" ]]; then
    echo 'Pass your QMK firmware checkout: bash firmware/build.sh /path/to/qmk_firmware' >&2
    exit 1
fi
mkdir -p "$qmk_home/keyboards/hc_macropad"
cp -R "$firmware_dir/keyboards/hc_macropad/." "$qmk_home/keyboards/hc_macropad/"
(cd "$qmk_home" && QMK_HOME="$qmk_home" qmk compile -kb hc_macropad -km default)
mkdir -p "$firmware_dir/dist"
cp "$qmk_home/hc_macropad_default.uf2" "$firmware_dir/dist/"
(cd "$firmware_dir/dist" && shasum -a 256 hc_macropad_default.uf2 > SHA256SUMS)
