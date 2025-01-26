import dotenv
import os
import cohere

dotenv.load_dotenv()

api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key)

response = co.embed(
    texts=["hello", "goodbye"], model="embed-english-v3.0", input_type="classification", embedding_types=["float"]
)
print(response.texts)
