import pytest
import os
import project.environment
import warnings


def tdd_EnvironmentConfig_class_creation():
    """
    GIVEN: setup.env_config import success
    WHEN: an EnvConfig object is instantiated
    THEN: an EnvConfig object is returned
    """
    env = project.environment.EnvironmentConfig()
    assert isinstance(env, project.environment.EnvironmentConfig)


def tdd_env_fixture_is_EnvironmentConfig(env):
    """
    GIVEN: an env tdd_fixture
    WHEN: env fixture is passed to a test
    THEN: env is an EnvConfig object
    """
    assert isinstance(env, project.environment.EnvironmentConfig)


def tdd_env_CONFIG_is_dictionary(env):
    """
    GIVEN: an env tdd_fixture
    WHEN: env fixture is passed to a test
    THEN: env CONFIG property is a dictionary
    """
    assert isinstance(env.CONFIG, dict)


def tdd_env_MODE_is_valid(env):
    """
    GIVEN: and env tdd_fixture
    WHEN: MODE is requested
    THEN: MODE is a valid value
    """
    valid_value_list = ['production', 'development', 'testing']
    assert any([env.MODE == valid for valid in valid_value_list])
    warn_value_list = ['development']
    if any([env.MODE == warn for warn in warn_value_list]):
        warnings.warn(UserWarning("mode is {} which should not be in production".format(env.MODE)))


def tdd_env_USER_HOME_isdir(env):
    """
    GIVEN: an env tdd fixture
    WHEN: env.USER_HOME is accessed
    THEN: a string pointing to a valid directory is returned
    """
    assert os.path.isdir(env.USER_HOME)


def tdd_env_ROOT_is_valid(env):
    """
    GIVEN: an env tdd_fixture
    WHEN: requesting
    ROOT property
    AND: return value is a directory
    THEN: directory contains 'tdd' and 'migration' directories
    AMD: directory contains an 'env.PROJECT_NAME' directory
    """
    assert os.path.isdir(env.ROOT)
    directory_contents = os.listdir(env.ROOT)
    assert any([item == 'tdd' for item in directory_contents])
    assert any([item == 'migrations' for item in directory_contents])
    assert any([item == env.PROJECT_NAME for item in directory_contents])


def tdd_env_HOSTNAME_is_str(env):
    """
    GIVEN: an env tdd_fixture
    WHEN: the type of env.HOSTNAME is requested
    THEN: it will be a string
    """
    assert isinstance(env.HOSTNAME, str)
