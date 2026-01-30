import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.parser import extract_text
from core.matcher import resume_score
from core.keyword_engine import missing_keywords
import threading
from llama_cpp import Llama
from docx import Document
from fpdf import FPDF

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ResumeAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Resume Analyzer AI")
        self.geometry("1000x700")

        self.resume_path = None

        # Initialize TinyLlama once
        self.llm = Llama(
            model_path=r"D:\llama\models\tinyllama-1.1b-1t-openorca.Q4_K_M.gguf",
            n_threads=2
        )

        tabs = ctk.CTkTabview(self)
        tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_analyze = tabs.add("Resume Match")
        self.tab_cover = tabs.add("Cover Letter")

        self.build_analyzer_tab()
        self.build_cover_letter_tab()

    # ---------- Resume Analyzer Tab ----------
    def build_analyzer_tab(self):
        ctk.CTkButton(
            self.tab_analyze, text="Upload Resume", command=self.upload_resume
        ).pack(pady=10)

        self.resume_label = ctk.CTkLabel(self.tab_analyze, text="No resume selected")
        self.resume_label.pack()

        ctk.CTkLabel(self.tab_analyze, text="Paste Job Description").pack(pady=10)

        self.jd_box = ctk.CTkTextbox(self.tab_analyze, height=200, width=900)
        self.jd_box.pack()

        ctk.CTkButton(
            self.tab_analyze, text="Analyze", command=self.analyze
        ).pack(pady=15)

        self.score_label = ctk.CTkLabel(self.tab_analyze, text="")
        self.score_label.pack()

        self.missing_label = ctk.CTkLabel(
            self.tab_analyze, text="", wraplength=900, justify="left"
        )
        self.missing_label.pack(pady=10)

    # ---------- Cover Letter Tab ----------
    def build_cover_letter_tab(self):
        # Generate button
        ctk.CTkButton(
            self.tab_cover, text="Generate Cover Letter", command=self.generate_letter
        ).pack(pady=10)

        # Text box to display cover letter
        self.cover_text = ctk.CTkTextbox(self.tab_cover, height=500, width=900)
        self.cover_text.pack(pady=10)

        # Save button
        ctk.CTkButton(
            self.tab_cover, text="Save Cover Letter", command=self.save_cover_letter
        ).pack(pady=10)

    # ---------- Actions ----------
    def upload_resume(self):
        self.resume_path = filedialog.askopenfilename(
            filetypes=[("PDF", "*.pdf"), ("Word", "*.docx")]
        )
        if self.resume_path:
            self.resume_label.configure(text=self.resume_path)

    def analyze(self):
        if not self.resume_path:
            self.score_label.configure(text="Upload a resume first")
            return

        jd_text = self.jd_box.get("1.0", "end").strip()
        if not jd_text:
            self.score_label.configure(text="Paste job description")
            return

        self.score_label.configure(text="Analyzing match...")
        self.missing_label.configure(text="")
        self.score_label.update_idletasks()

        resume_text = extract_text(self.resume_path)
        score = resume_score(resume_text, jd_text)
        missing = missing_keywords(resume_text, jd_text)

        self.score_label.configure(text=f"Match Score: {score}%")
        self.missing_label.configure(text="Missing Keywords:\n" + ", ".join(missing))

    def generate_letter(self):
        if not self.resume_path:
            self.cover_text.delete("1.0", "end")
            self.cover_text.insert("1.0", "Upload resume first")
            return

        jd_text = self.jd_box.get("1.0", "end").strip()
        if not jd_text:
            self.cover_text.delete("1.0", "end")
            self.cover_text.insert("1.0", "Paste job description first")
            return

        # Show immediate message
        self.cover_text.delete("1.0", "end")
        self.cover_text.insert("1.0", "Generating cover letter...\nPlease wait...")
        self.cover_text.update_idletasks()

        # Run generation in background thread
        threading.Thread(
            target=self._generate_letter_thread,
            args=(jd_text,),
            daemon=True
        ).start()


    def _generate_letter_thread(self, jd_text):
        try:
            # 1️⃣ Extract resume text
            resume_text = extract_text(self.resume_path)

            # 2️⃣ Reduce length to fit TinyLlama context window (512 tokens)
            # Approximate: 1 token ~ 4 chars, so 512 tokens ~ 2000 chars
            max_total_chars = 800
            resume_chars = max_total_chars // 2
            jd_chars = max_total_chars - resume_chars

            truncated_resume = resume_text[:resume_chars].strip()
            truncated_jd = jd_text[:jd_chars].strip()

            # 3️⃣ Build prompt
            prompt = (
                "Generate a human-friendly professional cover letter based on the following resume and job description.\n\n"
                f"Resume (truncated to fit model):\n{truncated_resume}\n\n"
                f"Job Description (truncated to fit model):\n{truncated_jd}\n\n"
                "Cover Letter:"
            )

            # 4️⃣ Generate with TinyLlama
            output = self.llm(
                prompt,
                max_tokens=300,    # smaller than context window to fit safely
                temperature=0.7,
                top_p=0.9
            )

            letter = output["choices"][0]["text"].strip()

            # 5️⃣ Update GUI safely
            self.cover_text.after(0, lambda: self._update_cover_text(letter))

        except Exception as e:
            self.cover_text.after(0, lambda e=e: self._update_cover_text(f"Error: {e}"))


    def _update_cover_text(self, letter):
        self.cover_text.delete("1.0", "end")
        self.cover_text.insert("1.0", letter)

    # ---------- Save Cover Letter ----------
    def save_cover_letter(self):
        letter = self.cover_text.get("1.0", "end").strip()
        if not letter:
            messagebox.showwarning("Warning", "No cover letter to save!")
            return

        # Ask user for file type and location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text File", "*.txt"),
                ("Word Document", "*.docx"),
                ("PDF File", "*.pdf")
            ]
        )
        if not file_path:
            return  # user cancelled

        try:
            if file_path.endswith(".txt"):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(letter)

            elif file_path.endswith(".docx"):
                doc = Document()
                doc.add_paragraph(letter)
                doc.save(file_path)

            elif file_path.endswith(".pdf"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)
                for line in letter.split("\n"):
                    pdf.multi_cell(0, 7, line)
                pdf.output(file_path)

            messagebox.showinfo("Saved", f"Cover letter saved to:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cover letter:\n{e}")


if __name__ == "__main__":
    app = ResumeAnalyzerApp()
    app.mainloop()
