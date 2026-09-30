# Optional utility commands to list all sound devices and default input device
# import sounddevice as sd
# print(sd.query_devices())
# print("Default input device:", sd.default.device)

import sounddevice as sd

# Inspect audio device details for device ID 15 (Microphone - Realtek Audio)
info = sd.query_devices(15)
print(info)