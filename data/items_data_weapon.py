from dataclasses import dataclass, field
from typing import List, Optional
import json

@dataclass
class CraftResource:
    uniquename: Optional[str]
    count: Optional[int]
    enchantmentlevel: Optional[int] = None

@dataclass
class CraftingRequirements:
    silver: Optional[int]
    time: Optional[float]
    craftingfocus: Optional[int]
    craftresource: List[CraftResource] = field(default_factory=list)

@dataclass
class CanHarvest:
    resourcetype: Optional[str]

@dataclass
class AudioInfo:
    name: Optional[str]

@dataclass
class SocketPreset:
    name: Optional[str]

@dataclass
class Item:
    uniquename: Optional[str]
    mesh: Optional[str]
    uisprite: Optional[str]
    maxqualitylevel: Optional[int]
    abilitypower: Optional[int]
    slottype: Optional[str]
    shopcategory: Optional[str]
    shopsubcategory1: Optional[str]
    attacktype: Optional[str]
    attackdamage: Optional[float]
    attackspeed: Optional[float]
    attackrange: Optional[float]
    twohanded: Optional[bool]
    tier: Optional[int]
    weight: Optional[float]
    activespellslots: Optional[int]
    passivespellslots: Optional[int]
    durability: Optional[int]
    durabilityloss_attack: Optional[int]
    durabilityloss_spelluse: Optional[int]
    durabilityloss_receivedattack: Optional[int]
    durabilityloss_receivedspell: Optional[int]
    mainhandanimationtype: Optional[str]
    unlockedtocraft: Optional[bool]
    unlockedtoequip: Optional[bool]
    itempower: Optional[int]
    unequipincombat: Optional[bool]
    uicraftsoundstart: Optional[str]
    uicraftsoundfinish: Optional[str]
    canbeovercharged: Optional[bool]
    canharvest: Optional[CanHarvest]
    craftingrequirements: Optional[CraftingRequirements]
    audioinfo: Optional[AudioInfo]
    socketpreset: Optional[SocketPreset]

def eliminar_prefijo_at(data):
    if isinstance(data, dict):
        return {key.lstrip('@'): eliminar_prefijo_at(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [eliminar_prefijo_at(item) for item in data]
    else:
        return data

def cargar_items_desde_archivo_weapon(file_path: str = 'data/items_data_weapon.json') -> List[Item]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
        
    if isinstance(data_list, dict):
        data_list = [data_list]
    data_list = [eliminar_prefijo_at(item) for item in data_list]

    items = []
    for data_dict in data_list:
        craftingrequirements_data = data_dict.get('craftingrequirements', {})
        if isinstance(craftingrequirements_data, list):
            craftingrequirements_data = craftingrequirements_data[0] if craftingrequirements_data else {}
        
        item = Item(
            uniquename=data_dict.get('uniquename'),
            mesh=data_dict.get('mesh'),
            uisprite=data_dict.get('uisprite'),
            maxqualitylevel=int(data_dict.get('maxqualitylevel', 0)),
            abilitypower=int(data_dict.get('abilitypower', 0)),
            slottype=data_dict.get('slottype'),
            shopcategory=data_dict.get('shopcategory'),
            shopsubcategory1=data_dict.get('shopsubcategory1'),
            attacktype=data_dict.get('attacktype'),
            attackdamage=float(data_dict.get('attackdamage', 0)),
            attackspeed=float(data_dict.get('attackspeed', 0)),
            attackrange=float(data_dict.get('attackrange', 0)),
            twohanded=data_dict.get('twohanded', 'false').lower() == 'true',
            tier=int(data_dict.get('tier', 0)),
            weight=float(data_dict.get('weight', 0)),
            activespellslots=int(data_dict.get('activespellslots', 0)),
            passivespellslots=int(data_dict.get('passivespellslots', 0)),
            durability=int(data_dict.get('durability', 0)),
            durabilityloss_attack=int(data_dict.get('durabilityloss_attack', 0)),
            durabilityloss_spelluse=int(data_dict.get('durabilityloss_spelluse', 0)),
            durabilityloss_receivedattack=int(data_dict.get('durabilityloss_receivedattack', 0)),
            durabilityloss_receivedspell=int(data_dict.get('durabilityloss_receivedspell', 0)),
            mainhandanimationtype=data_dict.get('mainhandanimationtype'),
            unlockedtocraft=data_dict.get('unlockedtocraft', 'false').lower() == 'true',
            unlockedtoequip=data_dict.get('unlockedtoequip', 'false').lower() == 'true',
            itempower=int(data_dict.get('itempower', 0)),
            unequipincombat=data_dict.get('unequipincombat', 'false').lower() == 'true',
            uicraftsoundstart=data_dict.get('uicraftsoundstart'),
            uicraftsoundfinish=data_dict.get('uicraftsoundfinish'),
            canbeovercharged=data_dict.get('canbeovercharged', 'false').lower() == 'true',
            canharvest=CanHarvest(
                resourcetype=data_dict.get('canharvest', {}).get('resourcetype')
            ) if 'canharvest' in data_dict else None,
            craftingrequirements=CraftingRequirements(
                silver=int(craftingrequirements_data.get('silver', 0)),
                time=float(craftingrequirements_data.get('time', 0)),
                craftingfocus=int(craftingrequirements_data.get('craftingfocus', 0)),
                craftresource=[
                    CraftResource(
                        uniquename=res.get('uniquename') if isinstance(res, dict) else None,
                        count=int(res.get('count', 0)) if isinstance(res, dict) else None,
                        enchantmentlevel=int(res.get('enchantmentlevel', 0)) if isinstance(res, dict) and 'enchantmentlevel' in res else None
                    ) for res in craftingrequirements_data.get('craftresource', [])
                ]
            ) if 'craftingrequirements' in data_dict else None,
            audioinfo=AudioInfo(
                name=data_dict.get('audioinfo', {}).get('name')
            ) if 'audioinfo' in data_dict else None,
            socketpreset=SocketPreset(
                name=data_dict.get('socketpreset', {}).get('name')
            ) if 'socketpreset' in data_dict else None
        )
        items.append(item)
    
    return items

'''file_path = 'data/items_data_weapon.json'
items = cargar_items_desde_archivo_weapon(file_path)'''