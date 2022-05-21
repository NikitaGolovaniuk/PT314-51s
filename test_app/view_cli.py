from view import View


class ViewCli(View):
    def __init__(self):
        pass

    def show_menu(self, settings):
        self.settings = settings
        choose = input(self.menu('main_menu'))
        match choose:
            case '1':
                val = input(self.menu('section_profile'))
                if int(val) in range(4): self.settings[0] = val 
            case '2':
                section_color = input(self.menu('section_color'))
                if int(section_color) in range(1,4):
                    match section_color:
                        case '1':
                            value = input('Left: ')
                            if self.verify_setting_list(value):
                                self.settings[1] = value 
                        case '2':
                            value = input('Midle: ')
                            if self.verify_setting_list(value):
                                self.settings[2] = value 
                        case '3':
                            value = input('Right: ')
                            if self.verify_setting_list(value):
                                self.settings[3] = value 
            case '3':
                val = input(self.menu('section_brightness'))
                if int(val) in range(0,101):
                    self.settings[4] = val
            case '4':
                val = input('format is x,x,x:\n')
                if self.verify_settings_val(val):
                    self.settings[5] = val
            case '5':
                section_fan = input(self.menu('section_fan'))
                if int(section_fan) in range(1,4) and int(self.settings[0]) in range(1,3):
                    match section_fan:
                        case '1':
                            self.settings[8] = '0'
                        case '2':
                            self.settings[8] = '1' 
                        case '3':
                            self.settings[8] = '3'
                            section_fan_custom = input(self.menu('section_fan_custom'))
                            if int(section_fan_custom) in range(1,4):
                                match section_fan_custom:
                                    case '1':
                                        val = input('set cpu fan speed:\n')
                                        if int(val) in range(0,101): self.settings[6] = val 
                                    case '2':
                                        val = input('set gpu fan speed:\n')
                                        if int(val) in range(0,101): self.settings[7] = val 
                                    case '3':
                                        val = input('set cpu+gppu fan speed:\n')
                                        if int(val) in range(0,101):  
                                            self.settings[7] = val
                                            self.settings[6] = val
                    return (self.settings, 1)
                else:
                    print("AVIABLE ONLY ON FIRST 2 PROFILES")
            case '6':
                print(self.my_menu['section_animation'])
            case '7':
                return (self.settings, 2)
        return (self.settings, 0)


    def menu(self, section):
        my_menu = {
        "main_menu": "1.Change profile\n2.Change color\n3.Change brightness\n4.Change keyboard lighting zone\n5.Set fan\n6.Set animation(currently unnaviable)\n7.Exit\n",
        "section_profile":  "0.Silent 1.Normal 2.Max 3.Turbo:\n",
        "section_color": "Keyboard color section 1-3:\n",
        "section_brightness": "0-100 brightness:\n",
        "section_animation": "NONENENENENE\n",
        "section_fan": "1.Silent\n2.Max\n3.Custom:\n",
        "section_fan_custom": "1.Left 2.Right 3,Both:\n",
        "section_exit": "Exit:\n",
        }
        return my_menu[section]

    def verify_setting_list(self, val):
        value = val.split(',')
        flag = True
        if len(value) != 3:
            flag = False
        for i in value:
            if int(i) < 0 or int(i) > 255:
                flag = False
        return flag

    def verify_settings_val(self, val):
        flag = True
        value = val.split(',')
        for i in value:
            if int(i) not in range(0,2):
                flag = False
        return flag

        
