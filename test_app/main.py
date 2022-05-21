

from model import Model
from controller import Controller
from view_cli import ViewCli
from settings.models.PT314_51S_715F import Data as curr_model



model = Model(curr_model())
view = ViewCli()
controller = Controller(model, view)


if __name__ == '__main__':
    controller.run()
    