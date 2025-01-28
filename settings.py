# -*- coding: utf-8 -*-

import yaml


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def load_settings(file_path='settings.yaml'):
    with open(file_path, 'r', encoding='utf-8') as file:
        settings = yaml.safe_load(file)
    return settings


@singleton
class Settings:
    def __init__(self, config_file='settings.yaml'):
        self.settings = load_settings(config_file)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value

    def __getattr__(self, item):
        return self.get(item)

