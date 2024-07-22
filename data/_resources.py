import os

def listar_archivos(path: str = 'data\\resources'):
    archivos = []
    for directorio_raiz, _, nombres_archivos in os.walk(path):
        for nombre_archivo in nombres_archivos:
            archivos.append(os.path.join(directorio_raiz, nombre_archivo))
    return archivos

def obtener_nombre_archivo_sin_extension(path: str):
    nombre_archivo, _ = os.path.splitext(os.path.basename(path))
    return nombre_archivo

def obtener_resources_id():
    ids = []
    paths = listar_archivos()
    for archivo in paths:
        ids.append(obtener_nombre_archivo_sin_extension(archivo))
    return ids

def obtener_resources_id_unicos():
    ids = obtener_resources_id()
    ids_unicos = [id for id in ids if '@' not in id]
    return ids_unicos

def dict_id_path():
    files = listar_archivos()
    list_id_path = []
    for path in files:
        id = obtener_nombre_archivo_sin_extension(path)
        list_id_path.append({'id': id, 'path': path})

    return list_id_path

'''ids = obtener_resources_id()
ids_unicos = obtener_resources_id_unicos()'''