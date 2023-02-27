""" @todo """
from hermes.gui.pages import AbstractPage


class BoardListPage(AbstractPage):

    def __init__(self) -> None:
        super().__init__(path='/boards', title='Mes cartes')

    def content(self) -> None:
        pass
