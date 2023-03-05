from nicegui.element import Element


class Container(Element):

    def __init__(self, tag: str = 'div') -> None:
        '''
        Container Element.

        Provides a container with a custom tag
        '''
        super().__init__(tag)
