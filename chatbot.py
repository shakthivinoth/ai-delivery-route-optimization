"""Module 2: Safety chatbot using TF-IDF + Cosine Similarity.
It only returns sentences that exist in policy/safety_policy.txt."""
import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity

NOT_FOUND = "I could not find this information in the company safety policy."
THRESHOLD = 0.15   # minimum similarity to accept an answer


def tokenize(text):
    """lowercase -> words -> remove stop words -> simple plural stripping."""
    text = text.lower().replace("seatbelt", "seat belt")
    words = re.findall(r"[a-z]+", text)
    return [w[:-1] if len(w) > 3 and w.endswith("s") else w
            for w in words if w not in ENGLISH_STOP_WORDS]


class SafetyChatbot:
    def __init__(self, policy_path):
        self.entries = []          # list of (section heading, sentence)
        heading = ""
        with open(policy_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    heading = line.lstrip("# ").strip()
                else:
                    self.entries.append((heading, line))
        docs = [f"{h} {s}" for h, s in self.entries]
        self.vectorizer = TfidfVectorizer(tokenizer=tokenize, lowercase=False,
                                          token_pattern=None)
        self.matrix = self.vectorizer.fit_transform(docs)

    def ask(self, question):
        if not question.strip():
            return {"answer": NOT_FOUND, "section": None, "score": 0.0}
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix)[0]
        best = int(scores.argmax())
        if scores[best] < THRESHOLD:
            return {"answer": NOT_FOUND, "section": None, "score": round(float(scores[best]), 3)}
        heading, sentence = self.entries[best]
        return {"answer": sentence, "section": heading, "score": round(float(scores[best]), 3)}
