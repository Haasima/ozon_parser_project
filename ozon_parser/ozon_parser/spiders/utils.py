import json
from typing import List

BLOCK_NAMES = ("Общие", "Дополнительные")
OS_PARAMS_NAMES = ("AndroidVersion", "iOSVer")

def get_characteristics(data_json: dict) -> list:
    """ Позволяет получить блок, содержащий характеристики товара """
    char_widget = None
    widgets_list = data_json["widgetStates"]
    for widget_name, widget_value in widgets_list.items():
        if "webCharacteristics" in widget_name:
            char_widget = widget_value
    widgets = json.loads(char_widget)
    return widgets.get("characteristics")

def get_cached_data(characteristics: list) -> list[dict]:
    """ Сохраняет в один список все параметры (словари) блоков, указанных в BLOCK_NAMES ("Общие", "Дополнительные") """
    cached_data = []
    for block in characteristics:
        block_name = block.get("title")
        if block_name in BLOCK_NAMES:
            cached_data.extend(block.get("short"))
    return cached_data

def get_os_version(cached_data: List[dict]) -> str:
    """ Достаёт из параметров ("AndroidVersion", "iOSVer") версию ОС """
    version = None
    for record in cached_data:
        current_key = record.get("key")
        if current_key in OS_PARAMS_NAMES:
            version = record.get("values")[0].get("text")
    return version if version else "Smartphones_without_version"

def parse_os_from_json(data_json: dict):
    """ Позволяет получить версию ОС смартфона """
    characteristics = get_characteristics(data_json=data_json)
    cached_data = get_cached_data(characteristics=characteristics)
    return get_os_version(cached_data=cached_data)
