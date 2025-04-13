import os
import numpy as np
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv
from lightrag.utils import EmbeddingFunc
from lightrag import LightRAG, QueryParam
from sentence_transformers import SentenceTransformer
from lightrag.kg.shared_storage import initialize_pipeline_status
import asyncio
import nest_asyncio


nest_asyncio.apply()

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

WORKING_DIR = "./dickens"

if os.path.exists(WORKING_DIR):
    import shutil

    shutil.rmtree(WORKING_DIR)

os.mkdir(WORKING_DIR)

async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    # 1. Initialize the GenAI Client with your Gemini API Key
    client = genai.Client(api_key=gemini_api_key)

    # 2. Combine prompts: system prompt, history, and user prompt
    if history_messages is None:
        history_messages = []

    combined_prompt = ""
    if system_prompt:
        combined_prompt += f"{system_prompt}\n"

    for msg in history_messages:
        # Each msg is expected to be a dict: {"role": "...", "content": "..."}
        combined_prompt += f"{msg['role']}: {msg['content']}\n"

    # Finally, add the new user prompt
    combined_prompt += f"user: {prompt}"

    # 3. Call the Gemini model
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[combined_prompt],
        config=types.GenerateContentConfig(max_output_tokens=500, temperature=0.1),
    )

    # 4. Return the response text
    return response.text


async def embedding_func(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings


async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=384,
            max_token_size=8192,
            func=embedding_func,
        ),
    )

    await rag.initialize_storages()
    await initialize_pipeline_status()

    return rag


def main():
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    text = "Once upon a time, high up in the blue sky, there lived a small fluffy cloud named Puffy. Puffy was not like the other clouds who liked to float in one place all day. Puffy was curious and loved adventures. One morning, Puffy looked down and saw a colorful hot air balloon floating over the mountains. 'I want to go on an adventure too!' Puffy said, puffing up with excitement. So Puffy asked the Wind, 'Will you take me to see the world?' The Wind laughed gently, 'Hop on! Let’s fly!' And off they went — whoooosh! First, they soared over a forest, where Puffy saw monkeys swinging from trees and parrots singing songs. Next, they floated over a desert, where camels marched in a line and the sand sparkled like gold under the sun. Then, they glided above the ocean, where Puffy made silly shapes in the sky and dolphins jumped up to say hello. Finally, Puffy reached a small village where the kids pointed up and said, 'Look! That cloud looks like a heart!' Puffy smiled. 'They noticed me!' After a long day, Puffy yawned. 'I think I’ll rest here for the night.' The Wind wrapped around him gently and said, 'Every day can be an adventure, little cloud. Just stay curious.' And so, Puffy drifted off to sleep, dreaming of mountains, deserts, oceans, and all the places he would visit next."

    rag.insert(text)

    response = rag.query(
        query="What was the name of the little cloud?",
        param=QueryParam(mode="hybrid", top_k=5, response_type="single line"),
    )

    print(response)

main()