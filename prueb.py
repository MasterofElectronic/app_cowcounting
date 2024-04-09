import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

directorio_credenciales = 'credentials_module.json'

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()
    return GoogleDrive(gauth)

def buscar(query):
    resultado = []
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        print('ID Drive', f['id'])
        resultado.append(f)
    return resultado

def descargar_archivo(id_archivo, ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    nombre_archivo = archivo['title']
    nombre_archivo = nombre_archivo.replace(':', '_')
    nombre_archivo = nombre_archivo.replace('/', '_')
    nombre_archivo = nombre_archivo.replace(' ', '_')
    ruta_completa = os.path.join(ruta_descarga, nombre_archivo)
    os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
    archivo.GetContentFile(ruta_completa)
    print("Descargado")

def borrar(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    archivo.Delete()

if __name__ == '__main__':
    archivos_encontrados = buscar("title contains 'vacamodelo'")
    for archivo in archivos_encontrados:
        descargar_archivo(archivo['id'], 'C:/Users/jhona/Documents/uis/cowcounting/imagenes/')
        print("Descargado")
