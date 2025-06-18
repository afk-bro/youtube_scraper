# src/distiller.py

import os
import requests

API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = os.getenv("PERPLEXITY_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def distill_with_perplexity(text: str, model="pplx-7b-chat") -> str:
    """
    Send a transcript chunk to Perplexity API for distillation.

    Parameters:
    - text (str): Raw transcript chunk
    - model (str): Model ID (default: pplx-7b-chat)

    Returns:
    - str: Clean summary
    """
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in trading strategies. Extract and summarize the key trading insight from this "
                    "transcript chunk, using clear language and proper ICT (Inner Circle Trader) terminology. Remove all fluff."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise RuntimeError(f"[Perplexity API Error {response.status_code}]: {response.text}")
