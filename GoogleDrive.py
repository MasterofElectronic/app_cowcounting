import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


directorio_credenciales = 'credentials_module.json'

#Iniciar Sesion 

def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)

#Buscar la imagen en el drive
def buscar(query):
    # Archivos con el nombre 'mooncode': title = 'mooncode'
    # Archivos que contengan 'mooncode' y 'mooncoders': title contains 'mooncode' and title contains 'mooncoders'
    # Archivos que NO contengan 'mooncode': not title contains 'mooncode'
    # Archivos que contengan 'mooncode' dentro del archivo: fullText contains 'mooncode'
    # Archivos en el basurero: trashed=true
    # Archivos que se llamen 'mooncode' y no esten en el basurero: title = 'mooncode' and trashed = false
    resultado = []
    credenciales = login()
    lista_archivos = credenciales.ListFile({'q': query}).GetList()
    for f in lista_archivos:
        print('ID Drive', f['id'])
        resultado.append(f)
    return resultado

#Descargar un archivo
def descargar_archivo(id_archivo, ruta_descarga):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    nombre_archivo = archivo['title']
    
    # Reemplazar caracteres no válidos en el nombre del archivo
    nombre_archivo = nombre_archivo.replace(':', '_')  # Reemplazar ':' con '_'
    nombre_archivo = nombre_archivo.replace('/', '_')
    nombre_archivo = nombre_archivo.replace(' ', '_')
    # Concatenar la ruta de descarga con el nombre del archivo modificado
    ruta_completa = os.path.join(ruta_descarga, nombre_archivo)
    
    # Crear los directorios si no existen
    os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
    
    archivo.GetContentFile(ruta_completa)

#borrar archivo
def borrar(id_archivo):
    credenciales = login()
    archivo = credenciales.CreateFile({'id': id_archivo})
    archivo.Delete()



if __name__ == '__main__':
    
    # Buscar archivos que contengan '.m._Img' en su título
    archivos_encontrados = buscar("title contains '2024'")
    
    # Descargar cada archivo encontrado
    for archivo in archivos_encontrados:
        descargar_archivo(archivo['id'], 'C:/Users/jhona/Documents/uis/cowcounting/imagenes/')
    #descargar_archivo(buscar("title contains '.m._Img'"),'C:/Users/jhona/Documents/uis/cowcounting/imagenes/')

    