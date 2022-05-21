class Data:
    def __init__(self):
        self.COLOR_REG_OFFSET = 0x3c        # keyboard color
        self.KEYBOARD_BRIGHTNESS = 0x19     # Brightness for full keyboard
        self.PROFILE_ONE = 0x2c             # Those values changes togather idk why
        self.PROFILE_TWO = 0x5c             # so i just copied both
        self.CPU_FAN_MODE = 0x21            # Auto/Max/Manual
        self.CPU_FAN_SPEED = 0x37           # 1-100 for manual mode
        self.GPU_FAN_MODE = 0x22            # Auto/Max/Manual
        self.GPU_FAN_SPEED = 0x3a           # 1-100 for manual mode
        self.TURBO_KEY_LIGHT = 0x5B 