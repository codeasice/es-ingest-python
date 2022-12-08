# https://codereview.stackexchange.com/questions/263215/how-to-handle-configuration-from-a-config-file-and-global-variables-transparentl
import json
from typing import Any, Dict
import logging

class Settings:

    DEFAULT_CONFIG = {
        'filenames_to_skip': {}
    }

    config = {}

    def __init__(self, config_file = 'settings.json'):
        self.config_file = config_file 

    def read_config(self) -> Dict[str, Any]:
        with open(self.config_file) as f:
            config_data = json.load(f)
            self.config.update(config_data)
            return self.config

    def get_setting(self, setting_name, default=None):
        tokens = setting_name.split(".")
        config = self.config

        for setting_name in tokens:
            if not(setting_name in config):
                if default is None:
                    logging.critical("Missing setting:" + setting_name)
                    exit(1) 
                else: 
                    return default
            value = config[setting_name]
            
            #Start searching from this node if there are more
            config = config[setting_name]
        return value

    def write_config(self, config: Dict[str, Any]) -> None:
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def has_setting(self, setting):
        return setting in self.config

    def load_or_default_config(self) -> None:
        try:
            self.config = self.read_config()
        except:
            logging.debug("Cant load settings file:" + self.config_file)
        else:
            logging.info("Succesfully loaded file:" + self.config_file)
        return self