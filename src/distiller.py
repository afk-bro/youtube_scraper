import subprocess

def distill_with_local_llm(text: str, model="mistral") -> str:
    """
    Use local Ollama model to distill trading-relevant transcript text.
    """
    prompt = (
        "Extract and summarize key trading insights from the following transcript chunk. "
        "Use ICT terminology where relevant. Remove filler, simplify language, and preserve high-signal content.\n\n"
        f"{text.strip()}"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode("utf-8").strip()
        return output
    except Exception as e:
        print(f"[ERROR] Local LLM distillation failed: {e}")
        return "[ERROR] Local LLM distillation failed."
