# resume_tinyllama_ai_app
Resume Analyzer using local tinyllama language model  .

Nutshell
Features of the App:
* Analyse Resume with target JD 
* FInd Missing keywords with JD 
* Write cover letter 


Features of the Application

1. Resume Analysis Against Target Job Description

    Performs an in-depth comparison between the candidate’s resume and the target Job Description (JD).
    
    Uses a locally hosted TinyLLaMA language model to understand contextual relevance, not just keyword matching.
    
    Evaluates alignment across skills, experience, tools, technologies, and role responsibilities.
    
    Provides an overall compatibility score indicating how well the resume matches the JD.

2. Missing Keywords & Skill Gap Identification

    Automatically extracts critical skills, technologies, and role-specific keywords from the JD.
    
    Identifies missing or underrepresented keywords in the resume.
    
    Highlights gaps in technical skills, soft skills, certifications, and domain-specific terms.
    
    Helps candidates optimize their resume for ATS (Applicant Tracking Systems).

3. AI-Generated Cover Letter

    Generates a customized cover letter tailored to the target JD and candidate’s resume.
    
    Ensures alignment with role requirements, company expectations, and industry tone.
    
    Supports multiple tones (formal, professional, concise, or enthusiastic).
    
    Eliminates generic content by producing role-specific and skill-focused narratives.

4. Local & Privacy-Focused AI Processing

    Runs entirely on a local TinyLLaMA model, ensuring data privacy and security.
    
    No resume or JD data is sent to external APIs or cloud services.
    
    Ideal for enterprise, offline, or privacy-sensitive environments.

5. Structured Resume Insights

    Breaks down resume content into structured sections such as:
    
    Skills
    
    Experience
    
    Education
    
    Certifications
    
    Provides actionable recommendations to improve clarity, relevance, and impact.

6. Fast & Lightweight Execution

    Optimized Python-based implementation for quick analysis.
    
    Minimal system resource usage compared to large cloud-based LLMs.
    
    Suitable for laptops and low-resource environments.

7. User-Friendly Workflow

    Simple input of resume and JD text or files.
    
    Clear, readable output with summaries, suggestions, and highlights.
    
    Easy to extend with additional features like scoring dashboards or export options.

🛠️ Tech Stack
Python
TinyLLaMA (local LLM)
NLP & text similarity techniques
Tokenization & keyword extraction
