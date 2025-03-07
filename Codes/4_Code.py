import dotenv
import os
from openai import OpenAI
import base64

dotenv.load_dotenv()
token = os.getenv("GITHUB_API_KEY")


endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
def get_image_data_url(image_file: str, image_format: str) -> str:
    """
    Helper function to converts an image file to a data URL string.

    Args:
        image_file (str): The path to the image file.
        image_format (str): The format of the image file.

    Returns:
        str: The data URL of the image.
    """
    try:
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Could not read '{image_file}'.")
        exit()
    return f"data:image/{image_format};base64,{image_data}"


client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that describes images in details.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image in French",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://cdn.britannica.com/25/172925-050-DC7E2298/black-cat-back.jpg",
                        "detail": "high"
                    },
                },
            ],
        },
    ],
    model=model_name,
)

print(response.choices[0].message.content)