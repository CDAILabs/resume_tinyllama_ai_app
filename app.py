import customtkinter as ctk
from llm.llama_mistral_client import LLMClient
from ui.main_window import ResumeAnalyzerApp

def main():
    # 1. Setup global appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # 2. Initialize the heavy model ONCE
    # Note: Use your path here
    model_path = r"D:\resume_mistral_ai_app\llama\models\mistral-7b-instruct-v0.2.Q2_K.gguf"
    llm_client = LLMClient(model_path=model_path)

    # 3. Start App
    app = ResumeAnalyzerApp(llm_client)
    app.mainloop()

if __name__ == "__main__":
    main()