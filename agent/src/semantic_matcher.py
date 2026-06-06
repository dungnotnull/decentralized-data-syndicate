import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

class SemanticMatcher:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        # In real run, this loads the model. For now, we stub the embedding process.
        self.model = None 
        self.model_name = model_name

    def get_embedding(self, text: str):
        # Simulated embedding vector (384-dim for bge-small)
        return np.random.rand(384)

    def find_best_matches(self, query_text: str, catalog_entries: List[Tuple[str, str]], threshold=0.7) -> List[str]:
        query_emb = self.get_embedding(query_text)
        results = []
        
        for entry_id, text in catalog_entries:
            entry_emb = self.get_embedding(text)
            similarity = np.dot(query_emb, entry_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(entry_emb))
            if similarity >= threshold:
                results.append((entry_id, similarity))
        
        # Sort by similarity descending
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results] 
