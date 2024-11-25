import sys
import pyautogui

if len(sys.argv) > 1:
    cmd = sys.argv[1]
    commands = [
    f'./run -c \"{cmd}\"'
    ]
else:
    commands = [
        './run'
    ]

pyautogui.hotkey('ctrl', 'shift', 't')

for part in commands:
    for char in part:
        if char == '/':
            pyautogui.hotkey('shift', '7') 
        elif char == ';':
            pyautogui.hotkey('shift', ',') 
        else:
            pyautogui.write(char)
pyautogui.press('enter')
