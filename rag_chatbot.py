from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class SimpleRAGChatbot:
    def __init__(self, kb):
        self.documents = kb.documents
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Fast and small
        self.generator_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.generator_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.corpus = [doc["text"] for doc in self.documents]
        self.corpus_embeddings = self.model.encode(self.corpus, convert_to_tensor=True)

    def generate_response(self, query: str) -> str:
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        hits = util.semantic_search(query_embedding, self.corpus_embeddings, top_k=5)[0]

        context = "\n".join([self.corpus[hit["corpus_id"]] for hit in hits])
        prompt = f"Answer the question based on the context.\nContext:\n{context}\nQuestion: {query}"

        inputs = self.generator_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.generator_model.generate(**inputs, max_new_tokens=150)
        return self.generator_tokenizer.decode(outputs[0], skip_special_tokens=True)
    def handle_query(self, query: str) -> str:
        if not query.strip():
            return "Please enter a valid query."
        if any(keyword in query.lower() for keyword in ['hello', 'hi', 'hey']):
            return "Hi! Ask me about restaurant menus, vegan options, prices, or compare spice levels."
        return self.generate_response(query)
