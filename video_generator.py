import re, os
import shutil
from requests import get
import urllib.request
from gtts import gTTS
from moviepy.editor import *
from openai import OpenAI
import requests
#ChatGPT API-KEY
client = OpenAI( api_key="")

#El texto
text = input("Sobre que tema quiere su cuento: ")
prompt = text

flask_api_url = "http://localhost:5000/image/"

#Generación de la historia
print("El BOT esta generando la historia")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Eres un profesional contando historias resumidas y cortas en 3 párrafos, escribir cuentos breves y cortos"},
    {"role": "user", "content": "genera una corta historia de no más de 600 caracteres o 120 palabras, separado en párrafos y comas sobre "},
    {"role": "user", "content": prompt},
  ]
)

print()

generated_text = completion.choices[0].message.content


# Split the text by , and .
paragraphs = re.split(r"[,.]", generated_text)

#Create Necessary Folders
if not os.path.exists("audio"):
    os.makedirs("audio")
if not os.path.exists("images"):
    os.makedirs("images")
if not os.path.exists("videos"):
    os.makedirs("videos")

# Loop through each paragraph and generate an image for each
i=1
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
    i+=1


clips = []
l_files = os.listdir("videos")
for file in l_files:
    clip = VideoFileClip(f"videos/{file}")
    clips.append(clip)

print("Concatenate All The Clips to Create a Final Video...")
final_video = concatenate_videoclips(clips, method="compose")
final_video = final_video.write_videofile("final_video.mp4")
print("The Final Video Has Been Created Successfully!")
shutil.rmtree("audio")
shutil.rmtree("images")
shutil.rmtree("videos")
