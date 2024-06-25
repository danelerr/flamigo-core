import requests


text = input()

text = "Responde en español. \nEres un maestro profesional, que enseña todo tipo de temas de manera efectiva.\n\n" + "genera una texto de no más de 500 caracteres o 100 palabras, separado en párrafos y comas que cree breve texto que enseñe algo de acuerdo a :\n\n" + text +"\n\n Responde simplemente con lo clave"



url = 'http://192.168.0.210:11434/api/generate' 

data = {
    'model': 'llama3',
    'prompt': text,
    'stream': False,
    'options': {
        'temperature': 1.0,
        # 'mirostat_tau': 2.0,
        # 'top_k': 10
    }
}

response = requests.post(url, json=data)


print(response.json()["response"])

