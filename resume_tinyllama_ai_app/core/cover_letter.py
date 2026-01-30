
from llm.llama_cpp_client import llama_generate

def generate_cover_letter(resume_text, jd_text):
    prompt = f"""
Write a natural, professional, human-sounding cover letter.
Avoid clichés and robotic phrases.
Keep it concise (3–4 paragraphs).

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    return llama_generate(prompt)
