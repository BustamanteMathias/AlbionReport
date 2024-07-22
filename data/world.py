import json
from typing import List
from dataclasses import dataclass

@dataclass
class SimpleItem:
    Index: str
    UniqueName: str

def cargar_items_desde_archivo(file_path: str) -> List[SimpleItem]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    items = [SimpleItem(**data) for data in data_list]
    return items


'''file_path = 'data/world.json'
items = cargar_items_desde_archivo(file_path)'''
