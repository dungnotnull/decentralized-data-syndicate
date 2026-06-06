# SECOND-KNOWLEDGE-BRAIN.md — decentralized-data-syndicate
*Self-improving knowledge base. Updated weekly via crawl4ai pipeline (Phase 4).*
*Last manual update: 2026-06-03*

---

## Core Concepts & Theoretical Foundations

### Zero-Knowledge Proofs (ZKPs)
A ZKP allows a prover to convince a verifier that a statement is true without revealing any information beyond the truth of the statement itself. Three key properties:
- **Completeness**: If the statement is true, the prover can always convince the verifier
- **Soundness**: If the statement is false, no cheating prover can convince the verifier (except with negligible probability)
- **Zero-knowledge**: The verifier learns nothing beyond the validity of the statement

**Key systems relevant to this project**:
- **Groth16**: Smallest proof size (192 bytes), fastest verification, requires per-circuit trusted setup. Best for on-chain verification. Used in our escrow verifier.
- **PLONK**: Universal trusted setup (one setup for all circuits), slightly larger proofs, more flexible. Good for evolving circuit designs.
- **STARKs**: No trusted setup (fully transparent), quantum-resistant, but large proof size (~100KB). Better for off-chain use.
- **Nova/SuperNova**: Recursive proof composition for incremental computation — relevant for streaming data subscriptions (Phase 5+ feature).

### Peer-to-Peer Networking (Libp2p)
Libp2p is a modular networking framework used by IPFS, Ethereum (devp2p successor), Polkadot, and Filecoin. Key components relevant to this project:
- **PeerID**: SHA-256 hash of a node's public key — the cryptographic identity of an agent
- **Kademlia DHT**: Distributed hash table for peer discovery and content routing
- **GossipSub**: Pub/sub messaging protocol with epidemic broadcast — used for `DataNeedSpec` broadcasts
- **libp2p Streams**: Multiplexed bidirectional streams for direct peer-to-peer data transfer

### Decentralized Marketplace Economics
- **Token-curated registries (TCRs)**: A token-weighted voting mechanism for maintaining quality lists — applicable to a curated list of reputable data sellers
- **Bonding curves**: Algorithmic pricing curves that adjust price based on supply — potential mechanism for data subscription pricing
- **Harberger Tax**: Self-assessed value with forced sale at that price — an alternative to fixed-price listings that keeps data available to willing buyers

### Data Quality Metrics
Standard metrics used in data engineering, formalized here for ZK attestation:
- **Completeness**: `(non_null_cells / total_cells) × 100%`
- **Uniqueness**: `(unique_rows / total_rows) × 100%`
- **Schema conformance**: All declared columns present with correct data types
- **Entropy**: Shannon entropy per column — low entropy indicates low information density (suspect padding/dummy data)
- **Distribution drift**: KL-divergence from a reference distribution — detects distribution shift between claimed and actual data

### Smart Contract Escrow Patterns
- **Two-phase commit**: Lock → verify → release (our pattern)
- **Optimistic release with dispute window**: Release funds automatically, allow disputes within N blocks — more user-friendly but requires on-chain arbitration
- **Streaming payments (Sablier)**: Continuous micro-payments per row transferred — suitable for large dataset streaming

---

## Key Research Papers

| Title | Authors | Year | Venue | Link | Relevance |
|-------|---------|------|-------|------|-----------|
| Groth16: On the Size of Pairing-based Non-interactive Arguments | Jens Groth | 2016 | EUROCRYPT | [IACR](https://eprint.iacr.org/2016/260) | ZK proof system used for on-chain quality verification |
| PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge | Gabizon, Williamson, Ciobotaru | 2019 | IACR | [IACR](https://eprint.iacr.org/2019/953) | Universal ZK proof system — alternative to Groth16 for flexible circuits |
| Libp2p: A Modular Peer-to-Peer Networking Stack | Protocol Labs | 2019 | IPFS Whitepaper | [GitHub](https://github.com/libp2p/specs) | Core P2P networking layer |
| Ocean Protocol: A Decentralized Substrate for AI Data & Services | Trent McConaghy et al. | 2019 | Whitepaper | [oceanprotocol.com](https://oceanprotocol.com/tech-whitepaper.pdf) | Directly relevant: decentralized data marketplace design patterns |
| IPFS — Content Addressed, Versioned, P2P File System | Juan Benet | 2014 | arXiv | [arXiv:1407.3561](https://arxiv.org/abs/1407.3561) | Data content addressing and immutable storage patterns |
| Filecoin: A Decentralized Storage Network | Protocol Labs | 2017 | Whitepaper | [filecoin.io](https://filecoin.io/filecoin.pdf) | Cryptographic proofs of storage — analogous to our proofs of data quality |
| zkSNARKs in a Nutshell | Christian Reitwiessner | 2016 | Ethereum Blog | [Ethereum.org](https://blog.ethereum.org/2016/12/05/zksnarks-in-a-nutshell) | Accessible ZK-SNARKs intro for Ethereum context |
| SnarkyJS and o1js: Writing ZK Circuits in TypeScript | Mina Protocol | 2023 | Mina Docs | [minaprotocol.com](https://minaprotocol.com) | TypeScript-native ZK framework — alternative to circom for TypeScript devs |
| Differential Privacy: A Survey of Results | Cynthia Dwork et al. | 2008 | TAMC | [Springer](https://doi.org/10.1007/978-3-540-79228-4_1) | Formal differential privacy — baseline theory for optional DP noise injection |
| The Moral Character of Cryptographic Work | Phillip Rogaway | 2015 | IACR | [IACR](https://eprint.iacr.org/2015/1162) | Ethics of cryptographic tools — relevant for responsible design of this system |
| FairSwap: How to Fairly Exchange Digital Goods | Stefan Dziembowski et al. | 2018 | ACM CCS | [ACM](https://dl.acm.org/doi/10.1145/3243734.3243857) | Trustless fair exchange protocol for digital goods — foundational to our escrow design |
| DECO: Liberating Web Data Using Decentralized Oracles for TLS | Zhang et al. | 2020 | ACM CCS | [ACM](https://dl.acm.org/doi/10.1145/3372297.3417239) | ZK proofs over TLS-secured web data — applicable to verifying data provenance from web sources |

---

## State-of-the-Art ML/DL Models

### Data Quality Assessment

| Model ID | Task | Benchmark | Notes |
|----------|------|-----------|-------|
| `microsoft/phi-3-mini-4k-instruct` | Structured quality report generation | MT-Bench: 8.38 | Primary local SLM; runs on CPU |
| `microsoft/phi-3.5-mini-instruct` | Quality report (improved) | MMLU: 69.0 | Successor to phi-3-mini; test if resource budget allows |
| `google/gemma-2-2b-it` | Lightweight quality assessment | MT-Bench: 7.74 | Alternative to Phi-3-mini; 2B params |
| `Qwen/Qwen2.5-1.5B-Instruct` | Ultra-lightweight quality checker | MMLU: 60.9 | For extremely resource-constrained environments |

### Semantic Embedding & Matching

| Model ID | Task | Benchmark (MTEB) | Notes |
|----------|------|------------------|-------|
| `BAAI/bge-small-en-v1.5` | Data catalog semantic search | MTEB avg: 62.17 | Primary embedding model; 33M params, fast |
| `BAAI/bge-m3` | Multilingual embedding | MTEB avg: 66.03 | If multilingual data catalogs needed; 568M params |
| `sentence-transformers/all-MiniLM-L6-v2` | Lightweight semantic matching | MTEB avg: 56.26 | Very fast; use for high-throughput matching |
| `mixedbread-ai/mxbai-embed-large-v1` | High-quality embedding | MTEB avg: 64.68 | If accuracy > speed; 335M params |

### ZK-Proof Tooling (Not ML — Cryptographic)

| Tool | Version | Purpose | Performance |
|------|---------|---------|------------|
| circom | 2.1.x | ZK circuit language and compiler | Compiles circuits to R1CS + WASM witness generator |
| snarkjs | 0.7.x | Groth16/PLONK proof generation and verification | ~10s for 100k constraints on CPU |
| rapidsnark | - | C++ prover for snarkjs circuits; 10–100x faster | Required for circuits > 1M constraints |
| bellman (Rust) | - | Rust ZK proving library — alternative backend | Used in zcash; most battle-tested |

---

## Tools, Libraries & Frameworks

| Tool/Library | Version | Purpose | Link |
|-------------|---------|---------|------|
| circom | 2.1.x | ZK circuit language; compiles to R1CS for snarkjs | [GitHub](https://github.com/iden3/circom) |
| snarkjs | 0.7.x | ZK proof generation (Groth16/PLONK), Solidity verifier export | [GitHub](https://github.com/iden3/snarkjs) |
| py-libp2p | 0.1.x | Python implementation of Libp2p | [GitHub](https://github.com/libp2p/py-libp2p) |
| js-libp2p | 1.x | Node.js implementation of Libp2p (more mature than py) | [GitHub](https://github.com/libp2p/js-libp2p) |
| Hardhat | 2.22.x | Ethereum development environment, local EVM node | [GitHub](https://github.com/NomicFoundation/hardhat) |
| OpenZeppelin Contracts | 5.x | Audited Solidity building blocks (ERC-20, access control) | [GitHub](https://github.com/OpenZeppelin/openzeppelin-contracts) |
| ethers.js | 6.x | Ethereum JSON-RPC client for JavaScript | [GitHub](https://github.com/ethers-io/ethers.js) |
| web3.py | 6.x | Ethereum JSON-RPC client for Python | [GitHub](https://github.com/ethereum/web3.py) |
| PyCryptodome | 3.20.x | AES-256-GCM, RSA, ECDSA in Python | [GitHub](https://github.com/Legrandin/pycryptodome) |
| PyNaCl | 1.5.x | X25519 ECDH key exchange, Ed25519 signatures | [GitHub](https://github.com/pyca/pynacl) |
| Ollama | 0.2.x | Local LLM server; runs Phi-3-mini and other models | [GitHub](https://github.com/ollama/ollama) |
| sentence-transformers | 3.x | Fast semantic embedding generation | [GitHub](https://github.com/UKPLab/sentence-transformers) |
| crawl4ai | 0.3.x | Async web crawler for research paper ingestion | [GitHub](https://github.com/unclecode/crawl4ai) |
| FastAPI | 0.111.x | Async REST API for agent local HTTP interface | [GitHub](https://github.com/tiangolo/fastapi) |
| Celery + Redis | 5.4 / 5.0 | Async task queue for ZK proof generation jobs | [GitHub](https://github.com/celery/celery) |
| Ocean Protocol SDK | 3.x | Reference implementation for decentralized data marketplace | [GitHub](https://github.com/oceanprotocol/ocean.py) |

---

## Self-Update Protocol

### Crawler Configuration (crawl4ai — Phase 4)

```python
# crawl4ai configuration for weekly research update
CRAWL_SOURCES = [
    {
        "name": "arxiv_cryptography",
        "url": "https://arxiv.org/list/cs.CR/recent",
        "keywords": ["zero-knowledge", "ZK-proof", "SNARK", "STARK", "data marketplace",
                     "decentralized data", "privacy-preserving", "verifiable computation"],
        "max_papers": 20
    },
    {
        "name": "arxiv_databases",
        "url": "https://arxiv.org/list/cs.DB/recent",
        "keywords": ["data quality", "data marketplace", "federated data", "data valuation",
                     "privacy-preserving data sharing"],
        "max_papers": 10
    },
    {
        "name": "huggingface_papers",
        "url": "https://huggingface.co/papers",
        "keywords": ["embedding", "text embedding", "data quality", "information retrieval"],
        "max_papers": 5
    },
    {
        "name": "ethresearch_zk",
        "url": "https://ethresear.ch/c/zkproofs/13",
        "keywords": ["ZK rollup", "proof system", "verifier contract", "data availability"],
        "max_papers": 10
    },
    {
        "name": "papers_with_code_zk",
        "url": "https://paperswithcode.com/search?q_meta=&q_type=&q=zero+knowledge",
        "keywords": ["zero-knowledge", "ZK", "verifiable"],
        "max_papers": 5
    }
]
```

### Domain-Specific Search Queries (Google Scholar / Semantic Scholar)
```
"zero-knowledge proof" AND "data marketplace"
"ZK-SNARK" AND "data quality" AND "verification"
"decentralized data trading" AND "smart contract"
"privacy-preserving data sharing" AND "blockchain"
"peer-to-peer data exchange" AND "cryptographic"
"data valuation" AND "federated learning"
"verifiable computation" AND "outsourced data"
circom circuit "data integrity"
"Groth16" AND "on-chain verifier" AND "data"
```

### Update Frequency
- **Research papers**: Weekly (every Monday 02:00 UTC)
- **HuggingFace model leaderboard check**: Weekly (check MTEB leaderboard for embedding model improvements)
- **Smart contract vulnerability feeds** (Rekt.news, SWC Registry): Weekly
- **Libp2p changelog**: Monthly (major version changes only)

### Format for New Entries
When adding a new paper to the Research Papers table, include:
```markdown
| [Title] | [Authors (first + et al.)] | [Year] | [Venue] | [DOI or arXiv link] | [1-sentence relevance note] |
```
Prepend `[AUTO-{DATE}]` to the relevance note for auto-added entries.

When adding a new model to the State-of-the-Art table:
```markdown
| `[model-id]` | [Task] | [Benchmark score] | [1-sentence comparison to current primary model] |
```

---

## Data Category Ontology
*Standardized tags for DataNeedSpec and seller catalog entries.*

```
data_category:
  behavioral:
    - api_usage_logs          # backend API call traces, parameters, latency
    - web_browsing_history    # URL visits, dwell time (anonymized)
    - app_usage_patterns      # app open/close events, feature usage
    - code_writing_patterns   # keystrokes, edit/delete ratios in IDEs
  financial:
    - transaction_history     # normalized payment records
    - spending_categories     # merchant category code distributions
    - portfolio_rebalancing   # asset allocation change events
  health:
    - activity_logs           # steps, heart rate, sleep (from wearables)
    - nutrition_logs          # meal logs, macro distributions
  location:
    - mobility_traces         # anonymized GPS traces
    - place_visit_frequency   # semantic location categories
  text:
    - personal_writing        # writing style samples, documents
    - search_queries          # query logs with category labels
    - conversation_logs       # anonymized chat patterns (turn length, etc.)
  sensory:
    - audio_features          # MFCC features only, no raw audio
    - image_embeddings        # embeddings only, no raw images
```

---

## Knowledge Update Log

| Date | Source | Type | Summary |
|------|--------|------|---------|
| 2026-06-03 | Manual initialization | Seed | Initial knowledge base created with ZKP fundamentals, Libp2p, Ocean Protocol, data quality metrics, and core tool inventory |

*Auto-entries will be added here by the crawl4ai pipeline starting in Phase 4 (Week 13–14).*
