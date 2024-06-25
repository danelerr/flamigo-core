import re
import os
import shutil
from flask import Flask, request, send_file
from requests import get
from gtts import gTTS
from moviepy.editor import *

import requests
from flask_cors import CORS

#from openai import OpenAI

app = Flask(__name__)
CORS(app)

flask_api_url = "http://177.222.103.79:5000/image/"

@app.route('/generar', methods=['POST'])
def generar_video():

    data = request.json
    prompt = data['prompt']
    name = data.get('name', 'final_video')

    print("El BOT esta generando la historia")


    prompt = "Responde en español. \nEres un maestro profesional, que enseña todo tipo de temas de manera efectiva.\n\n" + "genera una texto de no más de 500 caracteres o 100 palabras, separado en párrafos y comas que cree breve texto que enseñe algo de acuerdo a :\n\n" + prompt +"\n\n Responde simplemente con lo clave"

    url = 'http://177.222.103.79:11434/api/generate' 

    data = {
        'model': 'llama3',
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 1.0,
            # 'mirostat_tau': 2.0,
            # 'top_k': 10
    }
    }

    response = requests.post(url, json=data)

    #generated_text = completion.choices[0].message.content
    generated_text = response.json()["response"]

    # Split the text by , and .
    paragraphs = re.split(r"[,.]", generated_text)

    # Create Necessary Folders
    if not os.path.exists("audio"):
        os.makedirs("audio")
    else:
        shutil.rmtree("audio")
        os.makedirs("audio")
    if not os.path.exists("images"):
        os.makedirs("images")
    else:
        shutil.rmtree("images")
        os.makedirs("images")
    if not os.path.exists("videos"):
        os.makedirs("videos")
    else:
        shutil.rmtree("videos")
        os.makedirs("videos")


    # Loop through each paragraph and generate an image for each
    i = 1
    for para in paragraphs[:-1]:
        prompt = para.strip()

        response = requests.get(f"{flask_api_url}{prompt}")

        if response.status_code == 200:
            # Guardar la imagen recibida desde tu API Flask
            with open(f"images/image{i}.jpg", "wb") as f:
                f.write(response.content)
            print("The Generated Image Saved in Images Folder!")
        else:
            print("Failed to generate image from Flask API.")

        # Create gTTS instance and save to a file
        tts = gTTS(text=para, lang='es', slow=False)
        tts.save(f"audio/voiceover{i}.mp3")
        print("The Paragraph Converted into VoiceOver & Saved in Audio Folder!")

        # Load the audio file using moviepy
        print("Extract voiceover and get duration...")
        audio_clip = AudioFileClip(f"audio/voiceover{i}.mp3")
        audio_duration = audio_clip.duration

        # Load the image file using moviepy
        print("Extract Image Clip and Set Duration...")
        image_clip = ImageClip(f"images/image{i}.jpg").resize((512, 512)).set_duration(audio_duration)

        # Use moviepy to create a text clip from the text
        print("Customize The Text Clip...")

        def split_text_into_paragraphs(text, chunk_size=30):
            paragraphs = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            return "\n".join(paragraphs)
        
        tx_video = split_text_into_paragraphs(para.strip(), chunk_size=30)

        text_clip = TextClip(tx_video, fontsize=30, color="white")
        text_clip = text_clip.set_pos('center').set_duration(audio_duration)

        # Use moviepy to create a final video by concatenating
        # the audio, image, and text clips
        print("Concatenate Audio, Image, Text to Create Final Clip...")
        clip = image_clip.set_audio(audio_clip)
        video = CompositeVideoClip([clip, text_clip])

        # Save the final video to a file
        video = video.write_videofile(f"videos/video{i}.mp4", fps=24)
        print(f"The Video{i} Has Been Created Successfully!")
        i += 1

    clips = []
    l_files = os.listdir("videos")
    for file in l_files:
        clip = VideoFileClip(f"videos/{file}")
        clips.append(clip)

    print("Concatenate All The Clips to Create a Final Video...")
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.write_videofile(f"{name}.mp4")
    print("The Final Video Has Been Created Successfully!")




    return send_file(f"{name}.mp4")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
