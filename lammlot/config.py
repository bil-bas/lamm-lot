from cachetools import cached
from omegaconf import OmegaConf


@cached(cache={})
def get_config():
    return OmegaConf.load(config_path())


def save_config():
    OmegaConf.save(get_config(), config_path())


def config_path():
    return "./config.yaml"
