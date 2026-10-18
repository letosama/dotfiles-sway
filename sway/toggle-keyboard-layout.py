#!/usr/bin/env python3
"""Switch keyboard layouts and display the active layout through SwayOSD."""
import json
import subprocess


def sway(*args):
    result = subprocess.run(
        ["swaymsg", "-r", *args], check=True, capture_output=True, text=True
    )
    return json.loads(result.stdout)


result = sway("input", "type:keyboard", "xkb_switch_layout", "next")
if not all(item.get("success") for item in result):
    raise SystemExit("Could not switch keyboard layout.")

keyboards = [
    item for item in sway("-t", "get_inputs")
    if item["type"] == "keyboard" and item.get("xkb_active_layout_name")
]
if not keyboards:
    raise SystemExit("No keyboard layout found.")

layout = keyboards[0]["xkb_active_layout_name"]
subprocess.run(
    ["swayosd-client", "--custom-icon", "input-keyboard",
     "--custom-message", "Keyboard: " + layout],
    check=True,
)
