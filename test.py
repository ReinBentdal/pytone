import keyboard

# This function will be called every time a key is pressed
def on_key_event(e):
    print('Key:', e.name, ', Scan code:', e.scan_code)

# Hook the function
keyboard.hook(on_key_event)

# Enter a loop (this is necessary to keep the script running)
keyboard.wait()
