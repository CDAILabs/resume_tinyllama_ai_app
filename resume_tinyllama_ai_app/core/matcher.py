from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def resume_score(resume_text, jd_text):
    emb = model.encode([resume_text, jd_text])
    score = util.cos_sim(emb[0], emb[1]).item()
    return round(score * 100, 2)
