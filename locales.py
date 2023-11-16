# Loads the locality variables
import os
import json
LOCAL_DIR   : str  = "./locales"
LOCALES     : list = os.listdir(LOCAL_DIR)
locale_data : dict = {}

def find(self, lang):
    # Do a fuzzy search
    # i.e. deu will return de
    # Probably some overlaps somewhere! 
    for locale in self.LOCALES:
        if lang in locale.lower():
            return locale

def load(self, locale_file):
    if locale_file not in self.LOCALES:
        raise Exception(f"Invalid Locale file {locale_file}. File not found!")
    with open(os.path.join(self.LOCAL_DIR, locale_file)) as lf:
        return json.load(lf)

def translate(key, lang="en"):
    if not locale_data:
        locale_data =  load(find(lang) + ".json")
    if key in locale_data:
        return locale_data[key]
    raise Exception(f"Key {key} not found in locale file {os.path.join(LOCAL_DIR, lang.lower())}.json")

