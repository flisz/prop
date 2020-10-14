from flask_classful import FlaskView


__all__ = ('BaseView',)


class BaseView(FlaskView):
    @classmethod
    def __ignore__(cls):
        """Custom class attr that lets us control which models get ignored.

        We are using this because knowing whether or not we're actually dealing
        with an abstract base class is only possible late in the class's init
        lifecycle.

        This is used by the dynamic model loader to know if it should ignore.
        """
        return cls.__name__ in ('FlaskView', 'BaseView')  # can add more abstract base classes here

    def health(self):
        return "Healthy"