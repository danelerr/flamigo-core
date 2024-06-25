from flask import Flask, request, send_file
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Cargar el modelo y configurarlo
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda")

@app.route('/image/<text>', methods=['GET'])
def generate_image(text):
    width = 512  # Ancho deseado
    height = 512  # Alto deseado

    # Generar la imagen con el texto proporcionado
    prompt = text
    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0, width=width, height=height).images[0]

    # Convertir la imagen a bytes
    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    # Devolver la imagen al cliente
    return send_file(img_byte_array, mimetype='image/png')


@app.route('/mobile/', methods=['GET'])
def generate_mobile_image():
    # Obtener los parámetros de la solicitud
    prompt = request.args['prompt']
    unique = request.args['unique']

    width = 512  # Ancho deseado
    height = 512  # Alto deseado
    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0, width=width, height=height).images[0]

    # Convertir la imagen a bytes
    img_byte_array = BytesIO()
    image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    # Devolver la imagen al cliente
    return send_file(img_byte_array, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
