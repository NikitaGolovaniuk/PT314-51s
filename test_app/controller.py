
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.path_to_settings = '/home/ultrakill/my-pythond-development/acer-triton-300se/test_app/settings/user_settings'
    
    def run(self):
        curr_settings = self.read_user_settings(self.path_to_settings)
        new_settings = self.my_loop(curr_settings)
        self.write_user_settings(self.path_to_settings, new_settings)
        #self.model.load_settings(new_settings)        


    def read_user_settings(self, path_to_settings):
        with open(path_to_settings, 'r') as f:
            line = f.read().splitlines()
        return line


    def write_user_settings(self, path_to_settings, data):
        with open(path_to_settings, 'w') as f:
            for i in data:
                f.write(f"{i}\n")

    def my_loop(self, curr_settings):
        new_settings = curr_settings
        while True:
            response_list = self.view.show_menu(curr_settings)
            new_settings = response_list[0]
            match response_list[1]:
                case 0:
                    self.model.load_settings(new_settings)
                case 1:
                    self.model.fan_speed(new_settings)
                case 2:
                    break
        return new_settings

