from .mixins.base import BaseView


__all__ = ('ItemView',)


class ItemView(BaseView):

    def index(self):
        return "Hello"


