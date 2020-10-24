import os
import json
import sys
import platform
import yaml
from pathlib import Path

from project.setup.loggers import LOGGERS

log = LOGGERS.Setup


class SetupConfig:
    def __init__(self, config_yaml=None):
        self.__properties = dict()
        self.__properties['ROOT'] = self.__init_root()
        self.__properties['CONFIG'] = self.__init_config(config_yaml=config_yaml)
        self.__properties['DATABASE_INFO'] = self.__init_db_info()
        self.__properties['PROJECT_NAME'] = self.__init_project_name()
        self.__properties['MODE'] = self.__init_mode()
        self.__properties['HOSTNAME'] = self.__init_host_name()
        self.__properties['USER_HOME'] = self.__init_user_home()
        self.__properties['TEMPLATES'] = self.__init_templates()
        self.__properties['SECRET_KEY'] = self.__init_secret_key()

    @property
    def ROOT(self):
        return self.__properties['ROOT']

    @staticmethod
    def __init_root():
        levels_up = -2
        env_file_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        root = '/'.join(env_file_path.split('/')[:levels_up])
        sys.path.append(root)
        log.debug(f'ROOT: {root}')
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
                log.debug('CONFIG: Successfully loaded')
                log.debug(f'CONFIG: {json.dumps(data, indent=4)}')
                return data
        else:
            raise FileNotFoundError(f'{config_yaml} missing!')

    @property
    def DATABASE_INFO(self):
        return self.__properties['DATABASE_INFO']

    def __init_db_info(self):
        database_info_yaml = os.path.join(self.ROOT, 'db-info.yaml')
        data = dict()
        if os.path.isfile(database_info_yaml):
            with open(database_info_yaml) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                log.debug('SETUP.DATABASE_INFO: Successfully loaded')
                log.debug(f'SETUP.DATABASE_INFO: {json.dumps(data, indent=4)}')
                return data
        else:
            raise FileNotFoundError(f'{database_info_yaml} missing!')

    @property
    def PROJECT_NAME(self):
        return self.__properties['PROJECT_NAME']

    def __init_project_name(self):
        project_name = self.CONFIG.get('project_name')
        if project_name:
            log.debug(f'PROJECT_NAME: {project_name}')
            return project_name
        else:
            raise ValueError('project_name field missing from config.yaml')

    @property
    def MODE(self):
        return self.__properties['MODE']

    def __init_mode(self):
        mode = self.CONFIG.get('app', dict()).get('mode', 'development')
        log.debug(f'MODE: {mode}')
        return mode

    @property
    def USER_HOME(self):
        return self.__properties['USER_HOME']

    def __init_user_home(self):
        home = str(Path.home())
        log.debug(f'USER_HOME: {home}')
        return home

    @property
    def HOSTNAME(self):
        return self.__properties['HOSTNAME']

    def __init_host_name(self):
        hostname = platform.uname()[1].upper()
        log.debug(f'HOSTNAME: {hostname}')
        return hostname

    @property
    def TEMPLATES(self):
        return self.__properties['TEMPLATES']

    def __init_templates(self):
        templates = os.path.join(self.ROOT, self.PROJECT_NAME, 'templates')
        if os.path.isdir(templates):
            return templates
        else:
            raise NotADirectoryError(f'{templates} directory missing!')

    @property
    def SECRET_KEY(self):
        return self.__properties['SECRET_KEY']

    def __init_secret_key(self):
        secret_key = self.CONFIG.get('app', dict()).get('secret_key')
        if secret_key:
            log.debug(f'SECRET_KEY: {secret_key}')
            return secret_key
        else:
            raise ValueError('secret_key field missing from config.yaml')
