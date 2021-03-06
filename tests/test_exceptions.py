import os

import pytest

from modbot import DOTFILES
from modbot.config import Config, ConfigError
from modbot.modbot import add, remove
from tests import FILE, REPO_FILE


@pytest.mark.parametrize(
    'function, mocks, message',
    [
        (add, pytest.lazy_fixture('mock_modbot'), 'does not exist'),
        (add, pytest.lazy_fixture('mock_isfile'), 'already linked'),
        (remove, pytest.lazy_fixture('mock_modbot'), 'not in repo'),
        (remove, pytest.lazy_fixture('mock_isfile'), 'does not exist'),
    ],
)
def test_modbot_exceptions(function, mocks, message):
    with pytest.raises(OSError, match=message):
        function(mocks.config, REPO_FILE)


@pytest.mark.parametrize(
    'method, inputs, message',
    [
        (Config.add_link, ['~/' + FILE, REPO_FILE], 'already in config'),
        (Config.remove_link, [os.path.join(DOTFILES, '.fakefile')], 'not in config'),
    ],
)
def test_config_exceptions(mock_config, method, inputs, message):
    config = mock_config.config

    with pytest.raises(ConfigError, match=message):
        method(config, *inputs)
