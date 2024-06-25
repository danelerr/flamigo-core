from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
pipe.to("cuda")

prompt = "Un gato 3d "

width = 512  # Ancho deseado
height = 512  # Alto deseado

image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0, width=width, height=height).images[0]

image.save("output_image.png")
