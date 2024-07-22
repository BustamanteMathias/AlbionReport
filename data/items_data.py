import json

def cargar_items_desde_archivo_items_data(file_path: str = 'data/items_data.json'):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = json.load(file)
        data_list = data_list['items']
        equipment = data_list['equipmentitem']
        weapon = data_list['weapon']
        guardar_diccionario_en_json(equipment, 'items_data_equipment.json')
        guardar_diccionario_en_json(weapon, 'items_data_weapon.json')

def guardar_diccionario_en_json(diccionario, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(diccionario, file, ensure_ascii=False, indent=4)


'''file_path = 'data/items_data.json'
cargar_items_desde_archivo_items_data(file_path)'''
