import os
import sys

import dotbot

from . import HOME, LOG
from .config import Config


def add(config, filename, target=None, run=False):
    config = Config(config) if type(config) is str else config
    path, filename = os.path.split(filename)

    if not path:
        path = os.getcwd()

    if target is None:
        target = filename

    target_path, target = os.path.split(target)

    if not target:
        target = filename

    if not target_path:
        target_path = config.path
    elif config.path not in target_path:
        target_path = os.path.join(config.path, target_path)

    filename = os.path.join(path, filename)
    target = os.path.join(target_path, target)

    if not os.path.isfile(filename):
        raise OSError('File {} does not exist'.format(filename))

    if os.path.isfile(target):
        raise OSError('File {} already linked'.format(filename))

    config.add_link(filename.replace(HOME, '~'), target)
    config.save()

    LOG.info('Moving {2} from {1} to {0}'.format(target_path, *os.path.split(filename)))
    os.rename(filename, target)

    if run:
        run_dotbot(config.file)


def remove(config, filename, run=False):
    config = Config(config) if type(config) is str else config

    if config.path not in filename:
        filename = os.path.join(config.path, filename)

    if not os.path.isfile(filename):
        raise OSError('File {} not in repo'.format(filename))

    link = config.remove_link(os.path.relpath(filename, config.path))

    if not os.path.isfile(link):
        raise OSError('Link {} does not exist'.format(link))

    config.save()

    LOG.info('Moving {1} to {0}'.format(*os.path.split(link)))
    os.remove(link)
    os.rename(filename, link)

    if run:
        run_dotbot(config.file)


def run_dotbot(config_file):
    sys.argv[1:] = ['--config-file', config_file]
    dotbot.main()
