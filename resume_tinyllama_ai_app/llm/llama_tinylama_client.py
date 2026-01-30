import subprocess

# Paths (make sure these are correct)
LLAMA_PATH = r"D:\llama\llama-cli.exe"
MODEL_PATH = r"D:\llama\models\tinyllama-1.1b-1t-openorca.Q4_K_M.gguf"

def llama_generate(prompt, max_tokens=400, temp=0.7, top_p=0.9, timeout=120):
    """
    Generate text using TinyLlama model via llama-cli.

    Args:
        prompt (str): Input prompt for the model.
        max_tokens (int): Maximum tokens to generate.
        temp (float): Temperature for randomness.
        top_p (float): Top-p sampling.
        timeout (int): Subprocess timeout in seconds.

    Returns:
        str: Generated text from the model.
    """
    # Ensure prompt is safe
    safe_prompt = prompt.encode("utf-8", errors="ignore").decode("utf-8")

    # Build the command
    cmd = [
        LLAMA_PATH,
        "-m", MODEL_PATH,
        "-p", safe_prompt,
        "-n", str(max_tokens),
        "--temp", str(temp),
        "--top-p", str(top_p)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[Error] Generation timed out."
    except Exception as e:
        return f"[Error] {e}"

# Example usage
if __name__ == "__main__":
    prompt = "Write a short professional cover letter."
    output = llama_generate(prompt)
    print("=== Generated Output ===")
    print(output)

