import base64
import io
import subprocess
import time
from flask import Flask, jsonify, request
from PIL import Image
from ultralytics import YOLO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():


    if request.method == 'GET':
        # Ruta de la imagen local
        image_path = 'C:/Users/jhona/Documents/uis/cowcounting/imagenes/vacamodelo.jpg'

    # Cargar el modelo con los mejores pesos obtenidos y se define como model para usarlo posteriormente
        model = YOLO('C:/Users/jhona/Documents/uis/cowcounting/model_cow.pt')

    # Cargar la imagen localmente
        image = Image.open(image_path)

    # Realiza inferencia con el modelo YOLOv8n en la imagen
        result = model(image)

        num_b = 0  # Variable para número de cajas lo cual representará el número de vacas
        for r in result:
            num_b += len(r)

    # Generar imagen con las detecciones
        annotated_img = result[-1].plot()
    
    # Convertir la imagen a un objeto PIL.Image
        annotated_img_pil = Image.fromarray(annotated_img)

    # Convertir imagen resultante a base64
        img_buffer = io.BytesIO()
        annotated_img_pil.save(img_buffer, format="JPEG")

    # Convertir la imagen resultante a base64
        img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    # Crear el JSON de respuesta
        response_json = {
            'image_base64': img_str,
            'num_vacas': num_b
        }
        return jsonify(response_json)
    
    
    elif request.method == 'POST':
        base64_img = request.form['imagen']
        # Decodificar la imagen Base64
        img_data = base64.b64decode(base64_img)

        # Convertir la imagen decodificada a formato de imagen
        img = Image.open(io.BytesIO(img_data))

        # Guardar la imagen decodificada en una dirección específica
        img.save('C:/Users/jhona/Documents/uis/cowcounting/imagenes/vacamodelo.jpg')
        time.sleep(0.1)
        return 'Respuesta para el método POST'


    


    

    

if __name__ == '__main__':
    app.run(debug=True)


