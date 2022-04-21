import os
import sys
EC_IO="/sys/kernel/debug/ec/ec0/io"

os.system("modprobe -r ec_sys")
os.system("modprobe ec_sys write_support=1")

COLOR_REG_OFFSET = 0x3c        # keyboard color
KEYBOARD_BRIGHTNESS = 0x19     # Brightness for full keyboard
PROFILE_ONE = 0x2c             # Those values changes togather idk why
PROFILE_TWO = 0x5c             # so i just copied both
CPU_FAN_MODE = 0x21            # Auto/Max/Manual
CPU_FAN_SPEED = 0x37           # 1-100 for manual mode
GPU_FAN_MODE = 0x22            # Auto/Max/Manual
GPU_FAN_SPEED = 0x3a           # 1-100 for manual mode
TURBO_KEY_LIGHT = 0x5B         # Light of turbo button

"""
19 - 13
20 - 14
21 - 15
50 - 32
167 - A7
176 - B0
177 - B1
180 - B4
182 - B6
198 - C6
219 - DB
231 - E7
233 - E9
248 - F8
249 - F9
"""

idk_arr = ('13','14','15','32','A7','B0','B1','B4','B6','C6','DB','E7','E9','F8','F9')




def filter_char(char: int):
    if char<0 or char>255:
        raise Exception("it's not a single byte")
    return hex(char).encode()

def ec_read(offset):
    ec = os.open(EC_IO, os.O_RDONLY)
    os.lseek(ec, offset,0)
    byte=os.read(ec, 1)
    print(byte)
    os.close(ec)
    return ord(byte)

def ec_write(offset, value):
    value=clamp(value,255)
    value=value.to_bytes(1,byteorder="big")
    ec = os.open(EC_IO, os.O_RDWR )
    os.lseek(ec, offset,0)
    os.write(ec, value)
    os.close(ec)

def clamp(value, max):
    if value<0:
        value=0
    if value>max:
        value=max
    return value


def start():
    if ec_read(3) == 1:
        ec_write(3,0x11)

def stop():
    ec_write(3, 0x01)

def set_profile(value):

    if value == 0:  # quiet
        print('profile1')
        ec_write(PROFILE_ONE, 0)
        ec_write(PROFILE_TWO, 1)
        ec_write(CPU_FAN_MODE, 0x50)
        ec_write(GPU_FAN_MODE, 0x57)
        ec_write(TURBO_KEY_LIGHT, 0)
        return 0

    elif value == 1:  # normal
        print('profile2')
        ec_write(PROFILE_ONE, 1)
        ec_write(PROFILE_TWO, 2)
        ec_write(CPU_FAN_MODE, 0x50)
        ec_write(GPU_FAN_MODE, 0x57)
        ec_write(TURBO_KEY_LIGHT, 0)
        return 1

    elif value == 2:  # extreme
        print('profile3')
        ec_write(PROFILE_ONE, 4)
        ec_write(PROFILE_TWO, 3)
        ec_write(CPU_FAN_MODE, 0x50)
        ec_write(GPU_FAN_MODE, 0x57)
        ec_write(TURBO_KEY_LIGHT, 0)
        return 2

    else:  # TUURRBOOO
        ec_write(PROFILE_ONE, 5)
        ec_write(PROFILE_TWO, 4)
        ec_write(CPU_FAN_MODE, 0x60)
        ec_write(GPU_FAN_MODE, 0x5b)
        ec_write(TURBO_KEY_LIGHT, 1)
        return 3

def set_fan(curr_profile, mode, cpu_speed, gpu_speed):
    if curr_profile == 1 or curr_profile == 2:
        if mode == 0:
            ec_write(CPU_FAN_MODE, 0x50)
            ec_write(GPU_FAN_MODE, 0x57)
        elif mode == 1:
            ec_write(CPU_FAN_MODE, 0x60)
            ec_write(GPU_FAN_MODE, 0x5b)
        else:
            ec_write(CPU_FAN_MODE, 0x70)
            ec_write(GPU_FAN_MODE, 0x5f)
            ec_write(CPU_FAN_SPEED, cpu_speed)
            ec_write(GPU_FAN_SPEED, gpu_speed)
    else:
        print('Error')

def set_color(left_clr, midle_clr, right_clr):
    left_clr = (clamp(left_clr[0], 255), clamp(left_clr[1], 255), clamp(left_clr[2], 255))
    midle_clr = (clamp(midle_clr[0], 255), clamp(midle_clr[1], 255), clamp(midle_clr[2], 255))
    right_clr = (clamp(right_clr[0], 255), clamp(right_clr[1], 255), clamp(right_clr[2], 255))
    colors = [*left_clr, *midle_clr, *right_clr]
    for i in range(0,9):
        ec_write(COLOR_REG_OFFSET+i, colors[i])

def set_brightnes(br):
    br = clamp(br, 100)
    ec_write(KEYBOARD_BRIGHTNESS, br)

def set_keyboard_zone(l, m, r):
    val = "{0}{1}{2}".format(l, m, r)
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
    ec_write(31, _dict[val])

if __name__ == "__main__":
    #MENU -- Keyboard
    left_clr = (256, 0, 0)
    midle_clr = (0, 256, 0)
    right_clr = (256, 0, 0)
    br = 100

    set_color(left_clr, midle_clr, right_clr)
    set_keyboard_zone(1, 1, 1)
    set_brightnes(br)

    #Menu -- PROFILE [0-3] quiet. normal, extreme, turbo
    
    print('ARGUMENT --> ', sys.argv[1])
    mrange = ('0', '1', '2', '3')
    if sys.argv[1] in mrange:
        c_profile = set_profile(sys.argv[1])
    else:
        print('Wrong profile')

    start()
