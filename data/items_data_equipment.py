from dataclasses import dataclass, field
from typing import List, Optional
import json

@dataclass
class CraftResource:
    uniquename: Optional[str]
    count: Optional[float]
    enchantmentlevel: Optional[float] = None
    maxreturnamount: Optional[float] = None

@dataclass
class CraftingRequirements:
    silver: Optional[float]
    time: Optional[float]
    craftingfocus: Optional[float]
    craftresource: List[CraftResource] = field(default_factory=list)

@dataclass
class UpgradeRequirements:
    uniquename: Optional[str]
    count: Optional[float]

@dataclass
class Enchantment:
    enchantmentlevel: Optional[float]
    itempower: Optional[float]
    durability: Optional[float]
    craftingrequirements: List[CraftingRequirements] = field(default_factory=list)
    upgraderequirements: Optional[UpgradeRequirements] = None

@dataclass
class Item:
    uniquename: Optional[str]
    uisprite: Optional[str]
    maxqualitylevel: Optional[float]
    abilitypower: Optional[float]
    slottype: Optional[str]
    shopcategory: Optional[str]
    shopsubcategory1: Optional[str]
    tier: Optional[float]
    weight: Optional[float]
    activespellslots: Optional[float]
    passivespellslots: Optional[float]
    physicalarmor: Optional[float]
    magicresistance: Optional[float]
    durability: Optional[float]
    durabilityloss_attack: Optional[float]
    durabilityloss_spelluse: Optional[float]
    durabilityloss_receivedattack: Optional[float]
    durabilityloss_receivedspell: Optional[float]
    offhandanimationtype: Optional[str]
    unlockedtocraft: Optional[bool]
    unlockedtoequip: Optional[bool]
    hitpofloatsmax: Optional[float]
    hitpofloatsregenerationbonus: Optional[float]
    energymax: Optional[float]
    energyregenerationbonus: Optional[float]
    crowdcontrolresistance: Optional[float]
    itempower: Optional[float]
    physicalattackdamagebonus: Optional[float]
    magicattackdamagebonus: Optional[float]
    physicalspelldamagebonus: Optional[float]
    magicspelldamagebonus: Optional[float]
    healbonus: Optional[float]
    bonusccdurationvsplayers: Optional[float]
    bonusccdurationvsmobs: Optional[float]
    threatbonus: Optional[float]
    itempowerprogressiontype: Optional[str]
    magiccooldownreduction: Optional[float]
    bonusdefensevsplayers: Optional[float]
    bonusdefensevsmobs: Optional[float]
    magiccasttimereduction: Optional[float]
    attackspeedbonus: Optional[float]
    movespeedbonus: Optional[float]
    uicraftsoundstart: Optional[str]
    uicraftsoundfinish: Optional[str]
    healmodifier: Optional[float]
    craftingcategory: Optional[str]
    canbeovercharged: Optional[bool]
    showinmarketplace: Optional[bool]
    energycostreduction: Optional[float]
    masterymodifier: Optional[float]
    combatspecachievement: Optional[str] = None
    destinycraftfamefactor: Optional[float] = None
    socketpreset: Optional[str] = None
    craftingrequirements: List[CraftingRequirements] = field(default_factory=list)
    enchantments: List[Enchantment] = field(default_factory=list)

def eliminar_prefijo_at(data):
    if isinstance(data, dict):
        return {key.lstrip('@'): eliminar_prefijo_at(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [eliminar_prefijo_at(item) for item in data]
    else:
        return data

def cargar_items_desde_archivo_equipment(file_path: str = 'data/items_data_equipment.json') -> List[Item]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)

    data_list = eliminar_prefijo_at(data_list)

    items = []
    for data_dict in data_list:
        if not isinstance(data_dict, dict):
            continue

        craftingrequirements_data = data_dict.get('craftingrequirements', [])
        if isinstance(craftingrequirements_data, dict):
            craftingrequirements_data = [craftingrequirements_data]
        if isinstance(craftingrequirements_data, str):
            craftingrequirements_data = []

        enchantments_data = data_dict.get('enchantments', {}).get('enchantment', [])
        if isinstance(enchantments_data, dict):
            enchantments_data = [enchantments_data]
        if isinstance(enchantments_data, str):
            enchantments_data = []

        item = Item(
            uniquename=data_dict.get('uniquename'),
            uisprite=data_dict.get('uisprite'),
            maxqualitylevel=float(data_dict.get('maxqualitylevel', 0)),
            abilitypower=float(data_dict.get('abilitypower', 0)),
            slottype=data_dict.get('slottype'),
            shopcategory=data_dict.get('shopcategory'),
            shopsubcategory1=data_dict.get('shopsubcategory1'),
            tier=float(data_dict.get('tier', 0)),
            weight=float(data_dict.get('weight', 0)),
            activespellslots=float(data_dict.get('activespellslots', 0)),
            passivespellslots=float(data_dict.get('passivespellslots', 0)),
            physicalarmor=float(data_dict.get('physicalarmor', 0)),
            magicresistance=float(data_dict.get('magicresistance', 0)),
            durability=float(data_dict.get('durability', 0)),
            durabilityloss_attack=float(data_dict.get('durabilityloss_attack', 0)),
            durabilityloss_spelluse=float(data_dict.get('durabilityloss_spelluse', 0)),
            durabilityloss_receivedattack=float(data_dict.get('durabilityloss_receivedattack', 0)),
            durabilityloss_receivedspell=float(data_dict.get('durabilityloss_receivedspell', 0)),
            offhandanimationtype=data_dict.get('offhandanimationtype'),
            unlockedtocraft=data_dict.get('unlockedtocraft', 'false').lower() == 'true',
            unlockedtoequip=data_dict.get('unlockedtoequip', 'false').lower() == 'true',
            hitpofloatsmax=float(data_dict.get('hitpofloatsmax', 0)),
            hitpofloatsregenerationbonus=float(data_dict.get('hitpofloatsregenerationbonus', 0)),
            energymax=float(data_dict.get('energymax', 0)),
            energyregenerationbonus=float(data_dict.get('energyregenerationbonus', 0)),
            crowdcontrolresistance=float(data_dict.get('crowdcontrolresistance', 0)),
            itempower=float(data_dict.get('itempower', 0)),
            physicalattackdamagebonus=float(data_dict.get('physicalattackdamagebonus', 0)),
            magicattackdamagebonus=float(data_dict.get('magicattackdamagebonus', 0)),
            physicalspelldamagebonus=float(data_dict.get('physicalspelldamagebonus', 0)),
            magicspelldamagebonus=float(data_dict.get('magicspelldamagebonus', 0)),
            healbonus=float(data_dict.get('healbonus', 0)),
            bonusccdurationvsplayers=float(data_dict.get('bonusccdurationvsplayers', 0)),
            bonusccdurationvsmobs=float(data_dict.get('bonusccdurationvsmobs', 0)),
            threatbonus=float(data_dict.get('threatbonus', 0)),
            itempowerprogressiontype=data_dict.get('itempowerprogressiontype'),
            magiccooldownreduction=float(data_dict.get('magiccooldownreduction', 0)),
            bonusdefensevsplayers=float(data_dict.get('bonusdefensevsplayers', 0)),
            bonusdefensevsmobs=float(data_dict.get('bonusdefensevsmobs', 0)),
            magiccasttimereduction=float(data_dict.get('magiccasttimereduction', 0)),
            attackspeedbonus=float(data_dict.get('attackspeedbonus', 0)),
            movespeedbonus=float(data_dict.get('movespeedbonus', 0)),
            uicraftsoundstart=data_dict.get('uicraftsoundstart'),
            uicraftsoundfinish=data_dict.get('uicraftsoundfinish'),
            healmodifier=float(data_dict.get('healmodifier', 0)),
            craftingcategory=data_dict.get('craftingcategory'),
            canbeovercharged=data_dict.get('canbeovercharged', 'false').lower() == 'true',
            showinmarketplace=data_dict.get('showinmarketplace', 'false').lower() == 'true',
            energycostreduction=float(data_dict.get('energycostreduction', 0)),
            masterymodifier=float(data_dict.get('masterymodifier', 0)),
            combatspecachievement=data_dict.get('combatspecachievement'),
            destinycraftfamefactor=float(data_dict.get('destinycraftfamefactor', 0)) if 'destinycraftfamefactor' in data_dict else None,
            socketpreset=data_dict.get('socketpreset', {}).get('name', None),
            craftingrequirements=[
                CraftingRequirements(
                    silver=float(req.get('silver', 0)) if isinstance(req, dict) else None,
                    time=float(req.get('time', 0)) if isinstance(req, dict) else None,
                    craftingfocus=float(req.get('craftingfocus', 0)) if isinstance(req, dict) else None,
                    craftresource=[
                        CraftResource(
                            uniquename=res.get('uniquename', None) if isinstance(res, dict) else None,
                            count=float(res.get('count', 0)) if isinstance(res, dict) else None,
                            enchantmentlevel=float(res.get('enchantmentlevel', 0)) if isinstance(res, dict) and 'enchantmentlevel' in res else None,
                            maxreturnamount=float(res.get('maxreturnamount', 0)) if isinstance(res, dict) and 'maxreturnamount' in res else None
                        ) for res in req.get('craftresource', []) if isinstance(req, dict) and isinstance(res, dict)
                    ]
                ) for req in craftingrequirements_data if isinstance(req, dict)
            ],
            enchantments=[
                Enchantment(
                    enchantmentlevel=float(enc.get('enchantmentlevel', 0)) if isinstance(enc, dict) else None,
                    itempower=float(enc.get('itempower', 0)) if isinstance(enc, dict) else None,
                    durability=float(enc.get('durability', 0)) if isinstance(enc, dict) else None,
                    craftingrequirements=[
                        CraftingRequirements(
                            silver=float(req.get('silver', 0)) if isinstance(req, dict) else None,
                            time=float(req.get('time', 0)) if isinstance(req, dict) else None,
                            craftingfocus=float(req.get('craftingfocus', 0)) if isinstance(req, dict) else None,
                            craftresource=[
                                CraftResource(
                                    uniquename=res.get('uniquename', None) if isinstance(res, dict) else None,
                                    count=float(res.get('count', 0)) if isinstance(res, dict) else None,
                                    enchantmentlevel=float(res.get('enchantmentlevel', 0)) if isinstance(res, dict) and 'enchantmentlevel' in res else None,
                                    maxreturnamount=float(res.get('maxreturnamount', 0)) if isinstance(res, dict) and 'maxreturnamount' in res else None
                                ) for res in req.get('craftresource', []) if isinstance(req, dict) and isinstance(res, dict)
                            ]
                        ) for req in enc.get('craftingrequirements', []) if isinstance(enc, dict) and isinstance(req, dict)
                    ],
                    upgraderequirements=UpgradeRequirements(
                        uniquename=enc.get('upgraderequirements', {}).get('upgraderesource', {}).get('uniquename', None) if isinstance(enc, dict) else None,
                        count=float(enc.get('upgraderequirements', {}).get('upgraderesource', {}).get('count', 0)) if isinstance(enc, dict) else None
                    ) if isinstance(enc, dict) and 'upgraderequirements' in enc else None
                ) for enc in enchantments_data if isinstance(enc, dict)
            ]
        )
        items.append(item)

    return items


'''file_path = 'data/items_data_equipment.json'
items = cargar_items_desde_archivo_equipment(file_path)'''
