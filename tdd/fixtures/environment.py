import pytest

import project.environment


@pytest.fixture(scope='function')
def env():
    """
    Purpose: used for unit tests of env_config
    Returns: freshly instantiated env object for each test case
    """
    return project.environment.EnvironmentConfig()


@pytest.fixture
def ENV():
    """
    Purpose: used for testing outside of env_config
    Returns: env object instantiated at the end of the env_config import process
    """
    return project.environment.ENV
