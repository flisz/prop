import pytest

import project.setup


@pytest.fixture(scope='function')
def env():
    """
    Purpose: used for unit tests of setup/__init__.py
    Returns: freshly instantiated env object for each test case
    """
    return project.setup.SetupConfig()


@pytest.fixture
def ENV():
    """
    Purpose: used for testing outside of env_config
    Returns: env object instantiated at the end of the env_config import process
    """
    return project.environment.ENV
