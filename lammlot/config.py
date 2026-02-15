from cachetools import cached
from omegaconf import OmegaConf


@cached(cache={})
def get_config():
    return OmegaConf.load(config_path())


def save_config():
    OmegaConf.save(get_config(), config_path())


def config_path():
    return "./config.yaml"


@cached(cache={})
def get_secrets():
    return OmegaConf.load(secrets_path())


def save_secrets():
    OmegaConf.save(get_secrets(), secrets_path())


def secrets_path():
    return "./secrets.yaml"
