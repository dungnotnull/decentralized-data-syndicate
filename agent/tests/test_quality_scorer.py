import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Phase 0: validate that sentence-transformers + local model pipeline works
# Ollama/Phi-3-mini test requires running Ollama server locally.
# This script tests the embedding-based semantic matcher instead.

from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def test_semantic_matcher():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    buyer_need = "NestJS backend behavior logs with API latency and status codes"
    seller_catalog = [
        "Node.js API call traces including endpoint latency and HTTP status",
        "React frontend user interaction clickstream data",
        "PostgreSQL slow query logs and index usage statistics",
    ]

    buyer_emb = model.encode(buyer_need)
    seller_embs = model.encode(seller_catalog)

    scores = [cosine_similarity(buyer_emb, se) for se in seller_embs]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

    print(f"Buyer need: {buyer_need}");
    print(f"Top match: '{seller_catalog[ranked[0][0]]}' score={ranked[0][1]:.4f}");
    print(f"Second:    '{seller_catalog[ranked[1][0]]}' score={ranked[1][1]:.4f}");
    print(f"Third:     '{seller_catalog[ranked[2][0]]}' score={ranked[2][1]:.4f}");

    # Assert top match is the API traces entry
    assert ranked[0][0] == 0, "Expected API traces to rank first"
    assert ranked[0][1] > 0.5, "Expected top score > 0.5"
    print("PASS: Semantic matcher correctly ranks relevant datasets")

if __name__ == "__main__":
    test_semantic_matcher()
