import yaml


def load_settings(file_path='settings.yaml'):
    with open(file_path, 'r') as file:
        settings = yaml.safe_load(file)
    return settings
