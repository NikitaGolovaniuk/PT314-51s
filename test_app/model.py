import os
import sys


class Model:
    def __init__(self, notebook_model):
        os.system("modprobe -r ec_sys")
        os.system("modprobe ec_sys write_support=1")
        self.EC_IO = "/sys/kernel/debug/ec/ec0/io" 
        self.COLOR_REG_OFFSET = notebook_model.COLOR_REG_OFFSET        # keyboard color
        self.KEYBOARD_BRIGHTNESS = notebook_model.KEYBOARD_BRIGHTNESS     # Brightness for full keyboard
        self.PROFILE_ONE = notebook_model.PROFILE_ONE             # Those values changes togather idk why
        self.PROFILE_TWO = notebook_model.PROFILE_TWO             # so i just copied both
        self.CPU_FAN_MODE = notebook_model.CPU_FAN_MODE        # Auto/Max/Manual
        self.CPU_FAN_SPEED = notebook_model.CPU_FAN_SPEED           # 1-100 for manual mode
        self.GPU_FAN_MODE = notebook_model.GPU_FAN_MODE            # Auto/Max/Manual
        self.GPU_FAN_SPEED = notebook_model.GPU_FAN_SPEED   # 1-100 for manual mode
        self.TURBO_KEY_LIGHT = notebook_model.TURBO_KEY_LIGHT
    
    def filter_char(self, char: int):
        if char<0 or char>255:
            raise Exception("it's not a single byte")
        return hex(char).encode()

    def ec_read(self, offset):
        ec = os.open(self.EC_IO, os.O_RDONLY)
        os.lseek(ec, offset,0)
        byte=os.read(ec, 1)
        os.close(ec)
        return ord(byte)

    def ec_write(self, offset, value):
        value=self.clamp(value,255)
        value=value.to_bytes(1,byteorder="big")
        ec = os.open(self.EC_IO, os.O_RDWR )
        os.lseek(ec, offset,0)
        os.write(ec, value)
        os.close(ec)

    def clamp(self, value, max):
        if value<0:
            value=0
        if value>max:
            value=max
        return value


    def start(self):
        if self.ec_read(3) == 1:
            self.ec_write(3,0x11)

    def stop(self):
        self.ec_write(3, 0x01)

    def set_profile(self, value):
        value = int(value)
        
        if value == 0:  # quiet
            print('profile1')
            self.ec_write(self.PROFILE_ONE, 0)
            self.ec_write(self.PROFILE_TWO, 1)
            self.ec_write(self.CPU_FAN_MODE, 0x50)
            self.ec_write(self.GPU_FAN_MODE, 0x57)
            self.ec_write(self.TURBO_KEY_LIGHT, 0)

        elif value == 1:  # normal
            print('profile2')
            self.ec_write(self.PROFILE_ONE, 1)
            self.ec_write(self.PROFILE_TWO, 2)
            self.ec_write(self.CPU_FAN_MODE, 0x50)
            self.ec_write(self.GPU_FAN_MODE, 0x57)
            self.ec_write(self.TURBO_KEY_LIGHT, 0)

        elif value == 2:  # extreme
            print('profile3')
            self.ec_write(self.PROFILE_ONE, 4)
            self.ec_write(self.PROFILE_TWO, 3)
            self.ec_write(self.CPU_FAN_MODE, 0x50)
            self.ec_write(self.GPU_FAN_MODE, 0x57)
            self.ec_write(self.TURBO_KEY_LIGHT, 0)

        else:  # TUURRBOOO
            self.ec_write(self.PROFILE_ONE, 5)
            self.ec_write(self.PROFILE_TWO, 4)
            self.ec_write(self.CPU_FAN_MODE, 0x60)
            self.ec_write(self.GPU_FAN_MODE, 0x5b)
            self.ec_write(self.TURBO_KEY_LIGHT, 1)

    def set_fan(self, curr_profile, mode, cpu_speed, gpu_speed):
        if curr_profile == 1 or curr_profile == 2:
            if mode == 0:
                self.ec_write(self.CPU_FAN_MODE, 0x50)
                self.ec_write(self.GPU_FAN_MODE, 0x57)
            elif mode == 1:
                self.ec_write(self.CPU_FAN_MODE, 0x60)
                self.ec_write(self.GPU_FAN_MODE, 0x5b)
            else:
                self.ec_write(self.CPU_FAN_MODE, 0x70)
                self.ec_write(self.GPU_FAN_MODE, 0x5f)
                self.ec_write(self.CPU_FAN_SPEED, cpu_speed)
                self.ec_write(self.GPU_FAN_SPEED, gpu_speed)
        else:
            print('Error')

    def set_color(self, kb_color_list):
        print(kb_color_list)
        for i, item in enumerate(kb_color_list):
            self.ec_write(self.COLOR_REG_OFFSET+i, item)

    def set_brightnes(self, br):
        br = self.clamp(br, 100)
        self.ec_write(self.KEYBOARD_BRIGHTNESS, br)

    def set_keyboard_zone(self, kb_zlist):
        val = "{0}{1}{2}".format(kb_zlist[0], kb_zlist[1], kb_zlist[2])
        _dict = {
            '000': 0,
            '100': 1,
            '010': 2,
            '110': 3,
            '001': 4,
            '101': 5,
            '011': 6,
            '111': 7,
        }
        self.ec_write(31, _dict[val])
        
    def settings_to_int(self, sett_list):
        #moving through settings_list we bring back list there is ',' in line
        #or int(i) if not 
        return [[int(j) for j in i.split(',')] if (',' in i) else int(i) for i in sett_list]  
        


    def load_settings(self, settings):
        settings_int = self.settings_to_int(settings)
        self.set_profile(settings_int[0])
        self.set_color((*settings_int[1], *settings_int[2], *settings_int[3]))
        self.set_brightnes(settings_int[4])
        self.set_keyboard_zone(settings_int[5])
        self.start()

    def fan_speed(self, settings):
        settings_int = self.settings_to_int(settings)
        self.set_fan(settings_int[0], settings_int[8], settings_int[6], settings_int[7])
        self.start()
 




