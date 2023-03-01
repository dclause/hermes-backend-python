""" Board page. """

from hermes.gui import AbstractPage, pages


@pages.page(path='/board/{bid}')
class BoardPage(AbstractPage):
    """ Board list page """

    # pylint: disable-next=arguments-differ
    def create(self, bid: int):
        """
        :param bid: The board ID (from URL)
        """
        self.title = f'This is a test {bid}'
        super().build(bid)

    # pylint: disable-next=arguments-differ
    def content(self, bid: int) -> None:
        """
        :param bid: The board ID (from URL)
        """
