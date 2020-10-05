import logging
import os
import yaml


LOGGER_YAML_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'loggers.yaml')


with open(LOGGER_YAML_FILE_PATH) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(data)


class LoggerMetaProperty:
    @property
    def all(self):
        return type(self).all


class LoggerProperties(type):
    @property
    def all(cls):
        return [cls.Setup
                cls.WebApp,
                cls.Database]


class LOGGERS(LoggerMetaProperty, metaclass=LoggerProperties):
    Setup = logging.getLogger('Setup')
    WebApp = logging.getLogger('WebApp')
    Database = logging.getLogger('Database')
