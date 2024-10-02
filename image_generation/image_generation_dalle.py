import os
from openai import AzureOpenAI, OpenAIError
import json
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
 
load_dotenv()


def generate_image(prompt):

    client = AzureOpenAI(
        api_version=os.getenv('OPENAI_API_VERSION'),
        azure_endpoint=os.getenv('OPENAI_API_ENDPOINT'),
        api_key=os.getenv('OPENAI_API_KEY'),
    )

    try:
        response = client.images.generate(
            model="Dalle3",
            prompt=prompt,
            n=1,
            size="1024x1024" 
        )

        image_url = json.loads(response.model_dump_json())['data'][0]['url']
        return image_url
    
    except OpenAIError as e:
        print(f"Error to generate the image: {e}")
        return None

def store_image(url, image_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        
        image = Image.open(BytesIO(response.content))
        image = image.resize((1024, 1024), Image.Resampling.LANCZOS)

        # Salvar a imagem com alta qualidade
        image.save(image_path, format='PNG', quality=95)

        print(f"Save image in: {image_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error to download the image: {e}")
    except IOError as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    prompt = " a consultant home office in LEGO"

    image_url = generate_image(prompt)
    if image_url:
        store_image(image_url, "image_from_ai.png")
