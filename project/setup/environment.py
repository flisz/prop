import os
import sys
import platform
import yaml
from pathlib import Path
import shutil
import os

from project.loggers import LOGGERS

log = LOGGERS.Setup


class EnvironmentConfig:
    def __init__(self, config_yaml=None):
        self.__properties = dict()
        self.__properties['ROOT'] = self.__init_root()
        self.__properties['CONFIG'] = self.__init_config(config_yaml=config_yaml)
        self.__properties['PROJECT_NAME'] = self.__init_project_name()
        self.__properties['MODE'] = self.__init_mode()
        self.__properties['HOSTNAME'] = self.__init_host_name()
        self.__properties['USER_HOME'] = self.__init_user_home()

    @property
    def ROOT(self):
        return self.__properties['ROOT']

    @staticmethod
    def __init_root():
        levels_up = -2
        env_file_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        env_path_list = env_file_path.split('/')[:levels_up]
        root = os.path.join(tuple(env_path_list))
        sys.path.append(root)
        log.debug(f'ENV.ROOT: {root}')
        return root

    @property
    def CONFIG(self):
        return self.__properties['CONFIG']

    def __init_config(self, config_yaml=None):
        if not config_yaml:
            config_yaml = os.path.join(self.ROOT, 'config.yaml')
        data = dict()
        if os.path.isfile(config_yaml):
            with open(config_yaml) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                log.debug('ENV.CONFIG: Successfully loaded')
                return data
        else:
            raise FileNotFoundError(f'{config_yaml} missing!')

    @property
    def PROJECT_NAME(self):
        return self.__properties['PROJECT_NAME']

    def __init_project_name(self):
        project_name = self.CONFIG.get('project_name')
        if project_name:
            log.debug(f'ENV.PROJECT_NAME: {project_name}')
            return project_name
        else:
            raise ValueError('project_name field missing from config.yaml')

    @property
    def MODE(self):
        return self.__properties['MODE']

    def __init_mode(self):
        mode = self.CONFIG.get('ap').get('mode')
        log.debug(f'ENV.MODE: {mode}')
        return mode

    @property
    def USER_HOME(self):
        return self.__properties['USER_HOME']

    def __init_user_home(self):
        home = str(Path.home())
        log.debug(f'ENV.USER_HOME: {home}')
        return home

    @property
    def HOSTNAME(self):
        return self.__properties['HOSTNAME']

    def __init_host_name(self):
        hostname = platform.uname()[1].upper()
        log.debug(f'ENV.HOSTNAME: {hostname}')
        return hostname


ENV = EnvironmentConfig()
