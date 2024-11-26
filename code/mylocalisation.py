import json as _json
import myconfig as _config

loacalisation_data = ""
with open('./localization.json', 'r', encoding='utf-8') as file:
    loacalisation_data = _json.load(file)

current_locale_data = loacalisation_data[_config.language]
