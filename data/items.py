from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class Localization:
    EN_US: str
    DE_DE: str
    FR_FR: str
    RU_RU: str
    PL_PL: str
    ES_ES: str
    PT_BR: str
    IT_IT: str
    ZH_CN: str
    KO_KR: str
    JA_JP: str
    ZH_TW: str
    ID_ID: str
    TR_TR: str
    AR_SA: str

@dataclass
class ItemLocalization:
    LocalizationNameVariable: str
    LocalizationDescriptionVariable: str
    LocalizedNames: Localization
    LocalizedDescriptions: Optional[Localization]  # Allow None
    Index: str
    UniqueName: str

def convertir_claves(data):
    if isinstance(data, dict):
        return {key.replace("-", "_"): convertir_claves(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convertir_claves(item) for item in data]
    else:
        return data

def cargar_items_desde_archivo_items(file_path: str = 'data/items.json') -> List[ItemLocalization]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
    data_list = convertir_claves(data_list)
    
    items = []
    for data_dict in data_list:
        localized_names = data_dict.get('LocalizedNames')
        localized_descriptions = data_dict.get('LocalizedDescriptions')
        
        item_localization = ItemLocalization(
            LocalizationNameVariable=data_dict['LocalizationNameVariable'],
            LocalizationDescriptionVariable=data_dict['LocalizationDescriptionVariable'],
            LocalizedNames=Localization(**localized_names) if localized_names else None,
            LocalizedDescriptions=Localization(**localized_descriptions) if localized_descriptions else None,
            Index=data_dict['Index'],
            UniqueName=data_dict['UniqueName']
        )
        items.append(item_localization)
    
    return items


'''file_path = 'data/items.json'
items_localization = cargar_items_desde_archivo_items(file_path)'''

