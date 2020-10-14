from .mixins.base import BaseView


__all__ = ('RootView',)


class RootView(BaseView):
    route_base = '/'

    def index(self):
        return "Hello"

    def health(self):
        return "Healthy"
