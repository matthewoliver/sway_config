#!/usr/bin/env python3

import json
import subprocess
import sys

# get sway screens
result = subprocess.run(["swaymsg", "-t", "get_outputs", "-r"],
                        capture_output=True, text=True)

if not result.returncode and not result.stdout:
    sys.exit(1)

screens_data = json.loads(result.stdout)
left_screen = right_screen = None

for screen in screens_data:
    if not screen['active']:
        continue
    if screen['rect']['x'] == 0:
        left_screen = screen['name']
    else:
        right_screen = screen['name']

print(f'Left: {left_screen} Right: {right_screen}')

if not left_screen and not right_screen:
    sys.exit(2)

# Move sessions
sessions = {}
if all([left_screen, right_screen]):
    sessions[left_screen] = [1, 2, 3, 4, 5, 6]
    sessions[right_screen] = [7, 8, 9, 0]
else:
    screen = left_screen if left_screen else right_screen
    sessions[screen] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

for s, workspaces in sessions.items():
    for workspace in workspaces:
        res = subprocess.run(
            ['swaymsg', 'workspace', str(workspace), ',', 'move',
             'workspace', 'to', s], capture_output=True, text=True)
