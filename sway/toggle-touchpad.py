#!/usr/bin/env python3
import json
import subprocess


def sway(*args):
    result = subprocess.run(['swaymsg', '-r', *args], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def notify(message):
    subprocess.run(['notify-send', '-a', 'Touchpad', '-i', 'input-touchpad', '-t', '2000', '-h', 'string:x-canonical-private-synchronous:touchpad', 'Touchpad', message], check=True)


try:
    pads = [i for i in sway('-t', 'get_inputs') if i['type'] == 'touchpad']
    if not pads:
        notify('Touchpad not found.')
        raise SystemExit(1)
    target = 'enabled' if all(i.get('libinput', {}).get('send_events') == 'disabled' for i in pads) else 'disabled'
    result = sway('input', 'type:touchpad', 'events', target)
    if not all(r.get('success') for r in result):
        raise RuntimeError('Could not change touchpad settings.')
    pads = [i for i in sway('-t', 'get_inputs') if i['type'] == 'touchpad']
    if not pads or any(i.get('libinput', {}).get('send_events') != target for i in pads):
        raise RuntimeError('Could not verify touchpad status.')
    notify('Touchpad enabled.' if target == 'enabled' else 'Touchpad disabled.')
except (subprocess.SubprocessError, ValueError, RuntimeError) as error:
    notify('Operation failed: ' + str(error))
    raise SystemExit(1)
