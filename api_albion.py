from dataclasses import dataclass
from typing import List, Optional
import aiohttp
import asyncio
import re
from dataclasses import asdict
import pandas as pd
from data._resources import *

api_host_europe = 'https://europe.albion-online-data.com'
api_host_asia = 'https://east.albion-online-data.com'
api_host_americas = 'https://west.albion-online-data.com'

@dataclass
class ItemPrice:
    item_id: str
    city: str
    quality: str  
    sell_price_min: int
    sell_price_min_date: str
    sell_price_max: int
    sell_price_max_date: str
    buy_price_min: int
    buy_price_min_date: str
    buy_price_max: int
    buy_price_max_date: str
    localized_name_es: Optional[str] = None
    localized_name_en: Optional[str] = None
    tier: Optional[str] = None
    '''path: Optional[str] = None'''

def quality_to_text(quality: int) -> str:
    quality_mapping = {
        1: "Normal",
        2: "Bueno",
        3: "Notable",
        4: "Sobresaliente",
        5: "Obra Maestra"
    }
    return quality_mapping.get(quality, "Desconocido")

def extract_tier(item_id: str) -> str:
    match = re.match(r"^(.{2}).*(.{2})$", item_id)
    if match:
        first_chars = match.group(1)
        last_chars = match.group(2)
        if '@' in last_chars:
            last_chars = last_chars.replace('@', '.')
        else:
            last_chars = ''
        return f'{first_chars}{last_chars}'
    return None

async def fetch_item_prices(item_id: str, locations: str) -> Optional[List[ItemPrice]]:
    api_host = api_host_europe
    endpoint = f'/api/v2/stats/Prices/{item_id}.json'
    url = f'{api_host}{endpoint}'
    params = {'locations': locations, 'qualities': '1,2,3,4,5'}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return [ItemPrice(**item) for item in data]
        except aiohttp.ClientError:
            return None

def get_item_prices(item_id: str, locations: str) -> Optional[List[ItemPrice]]:
    return asyncio.run(fetch_item_prices(item_id, locations))

def get_dict_id_path():
    return dict_id_path()

def merge_additional_info(items: List[ItemPrice], additional_info: List[dict]) -> List[ItemPrice]:
    info_dict = {info['UniqueName']: info for info in additional_info}
    info_path = get_dict_id_path()

    for item in items:
        item.tier = extract_tier(item.item_id)
        item.quality = quality_to_text(item.quality)
        '''for item in items:
            for dic in info_path:
                if item.item_id == dic['id']:
                    item.path = dic['path']
                    break'''
        
        if item.item_id in info_dict:
            item_info = info_dict[item.item_id]
            item.localized_name_es = item_info['LocalizedNames'].get('ES-ES', None)
            item.localized_name_en = item_info['LocalizedNames'].get('EN-US', None)
    return items

def guardar_en_excel(items: List[ItemPrice], file_path: str):
    df = pd.DataFrame([asdict(item) for item in items])
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        ciudades = df['city'].unique()
        for ciudad in ciudades:
            df_ciudad = df[df['city'] == ciudad].copy()
            df_ciudad.drop(columns=['item_id', 'city', 'sell_price_max', 'sell_price_max_date', 'buy_price_min', 'buy_price_min_date'], inplace=True) 
            df_ciudad.rename(columns={
                'localized_name_es': 'Name ES', 
                'tier': 'Tier', 
                'quality': 'Quality', 
                'sell_price_min': 'Sell MIN', 
                'sell_price_min_date': 'Sell Update', 
                'buy_price_max': 'Buy MAX', 
                'buy_price_max_date': 'Buy Update', 
                'localized_name_en': 'Name EN'
            }, inplace=True)
            column_order = [
                'Name ES', 'Name EN', 'Tier', 'Quality',
                'Sell MIN', 'Sell Update', 'Buy MAX', 'Buy Update'
            ]
            df_ciudad = df_ciudad[column_order]
            df_ciudad.to_excel(writer, sheet_name=ciudad, index=False)
