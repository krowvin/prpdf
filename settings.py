"""
PR PDF

settings - Helpers

2020 maschhoff github.com/maschhoff

"""

import logging
import json
import os
from vars import WORK_DIR
logger = logging.getLogger(__name__)
CONFIG_FILE = os.path.join(WORK_DIR, 'config\config.json')
DEFAULT_CONFIG = """{
    "port":80,
    "debug":"off",
    "lang":"en",
    "updatetime":1800,
    "index":{
        "Foldername/Filename":["Keyword1"],
        "Foldername2/Filename":["Keyword1","Keyword2 ","Keyword3"]
    }
}"""
# or '/data/prpdf/config/config.json'

def readConfig():
	with open(CONFIG_FILE, 'r') as cf:
		return cf.read()

def loadConfig():
    #print("loadConfig()")
    try:
        if not os.path.exists(CONFIG_FILE):
            writeConfig(DEFAULT_CONFIG)
        with open(CONFIG_FILE, 'r') as fp:
            return json.load(fp)
    except FileNotFoundError:
        logger.warning(f"File Not Found {CONFIG_FILE}")
        return {}

def writeConfig(config_data, config_file=CONFIG_FILE):
    '''
        Writes a dictionary or string object to a config file

        Takes optional config file path
    '''
    with open(config_file, "w") as cfg_file:
        if isinstance(config_data, dict):
            json.dump(config_data, cfg_file)
        else:
            cfg_file.write(config_data)
        logger.info(f"Configuration updated ({config_file}")
