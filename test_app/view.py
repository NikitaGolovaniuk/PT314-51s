from abc import ABC, abstractmethod


class View(ABC):

    @abstractmethod
    def show_menu(self, settings):
        raise NotImplementedError


   