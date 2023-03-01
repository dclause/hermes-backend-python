from nicegui.elements.mixins.text_element import TextElement


class Tag(TextElement):
    """ Displays some text, wrapped in custom tag. """

    def __init__(self, *, tag: str = 'div', text: str = '', **kwargs) -> None:
        """
        :param tag: the tag to be used
        :param text: the content of the tag
        """
        super().__init__(tag=tag, text=text)
