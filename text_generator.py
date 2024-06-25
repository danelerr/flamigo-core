from openai import OpenAI

client = OpenAI( api_key="")


# Set the prompt to generate text for
text = input("Sobre que tema quiere su cuento: ")
prompt = text

print("El boto esta generando la historia")
# Generate text using the GPT-3 model



completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Eres un profesional contando historias resumidas y cortas en 3 párrafos, escribir cuentos breves y cortos"},
    {"role": "user", "content": "genera una corta historia de no más de 500 caracteres o 100 palabras, separado en párrafos y comas sobre "},
    {"role": "user", "content": prompt},
  ]
)
print()
# Print the generated text
generated_text = completion.choices[0].message.content

print(generated_text)
# Save the text in a file
with open("generated_text.txt", "w") as file:
    file.write(generated_text.strip())

print("La historia se ha generado exitosamente")
