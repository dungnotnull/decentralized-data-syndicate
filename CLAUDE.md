# CLAUDE.md — decentralized-data-syndicate

## Project Identity
- **Name**: decentralized-data-syndicate
- **Tagline**: A P2P agent network for buying and selling clean, verified data with crypto payments and ZK-Proof quality guarantees
- **Status**: Phase 0 COMPLETE -> Ready for Phase 1
- **Cluster**: A — Decentralized Agent Infrastructure (alongside Folders 1 and 7)

---

## Core Problem
Centralized data brokers extract enormous value from user-generated data while giving users no control, no payment, and no transparency. Meanwhile, AI model trainers and data scientists struggle to obtain high-quality, domain-specific datasets at reasonable cost. This project builds a peer-to-peer data marketplace where personal AI agents can discover, negotiate, and transact data assets autonomously — with Zero-Knowledge Proofs guaranteeing data quality without exposing raw content, Smart Contracts enforcing payment escrow, and a mandatory human-in-the-loop gate before any data leaves a user's control.

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│  Libp2p P2P Network (Discovery, Messaging, DHT)         │
│  ┌────────────────┐         ┌────────────────────────┐  │
│  │  Buyer Agent   │◄──────►│   Seller Agent          │  │
│  │  (Data Seeker) │  JSON  │   (Data Provider)       │  │
│  └───────┬────────┘ Offer  └────────┬───────────────┘  │
│          │                           │ Human Approval    │
│          │                           │ Pop-up Gate       │
│  ┌───────▼────────────────────────────────────────────┐ │
│  │        Smart Contract (Escrow + Settlement)        │ │
│  │        EVM-compatible (Hardhat / Ethereum / L2)    │ │
│  └───────┬────────────────────────────────────────────┘ │
│          │                                               │
│  ┌───────▼──────────┐    ┌─────────────────────────┐    │
│  │  ZK-Proof Engine │    │  Local SLM Quality       │    │
│  │  (Data Quality   │    │  Scorer (noise, schema,  │    │
│  │   Verification)  │    │  completeness)           │    │
│  └──────────────────┘    └─────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Platform**: Python 3.11+ backend, React frontend (buyer/seller dashboards), Node.js blockchain scripts
**ML Stack**: Local SLM for data quality scoring, ZK-SNARK circuit for quality attestation
**Local SLM**: Phi-3-mini or similar, runs fully offline for data quality assessment
**External APIs**: Claude API / GPT-4o as optional natural language query translator only

---

## Key Technical Decisions

1. **Deterministic protocol core**: All discovery, negotiation, escrow, and settlement messages use strict Protobuf/JSON-Schema. No natural language at the protocol layer.
2. **ZK-Proofs for quality, not content**: Buyers verify statistical properties (schema compliance, null rate, row count, column entropy) without seeing raw data. This is the critical privacy guarantee.
3. **Libp2p for P2P networking**: Same stack as Folder 1 for protocol-level compatibility. Peer discovery via mDNS (local) and Kademlia DHT (global).
4. **EVM-compatible smart contracts**: Escrow contract deployed on an EVM L2 (Polygon/Arbitrum) to minimize gas fees. Hardhat for local development.
5. **Human-in-the-loop is a hard gate**: Seller-side agent cannot transmit data without explicit human approval. Approval event is logged on-chain (hash only).
6. **AES-256-GCM end-to-end encryption**: Data payload encrypted with buyer's public key before transmission. Decryption key released only after contract settlement.
7. **Local SLM as quality pre-filter**: Before ZK circuit runs, local SLM performs a lightweight quality check to avoid wasting ZK compute on obviously bad data.
8. **No central discovery server**: Relies on Libp2p DHT and gossip protocols. Optional relay nodes for NAT traversal only.

---

## External LLM API Integrations

| Provider | Purpose | Config Key | Required? |
|----------|---------|-----------|-----------|
| Anthropic Claude API | Natural language → structured data-need query translation | `CLAUDE_API_KEY` | Optional |
| OpenAI GPT-4o | Fallback NL query translator | `OPENAI_API_KEY` | Optional |
| Local Ollama (Phi-3-mini) | Data quality scoring, schema inference, local reasoning | `OLLAMA_BASE_URL` | Recommended |

LLM provider selection: `LLM_PROVIDER=claude|openai|ollama` (default: `ollama`)

---

## HuggingFace Models In Use

| Model ID | Purpose | Link |
|----------|---------|------|
| `microsoft/phi-3-mini-4k-instruct` | Local SLM — data quality scoring, schema inference | [HF](https://huggingface.co/microsoft/phi-3-mini-4k-instruct) |
| `sentence-transformers/all-MiniLM-L6-v2` | Semantic embedding for data-need matching (buyer ↔ seller topic alignment) | [HF](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| `BAAI/bge-small-en-v1.5` | Lightweight embedding for data catalog search | [HF](https://huggingface.co/BAAI/bge-small-en-v1.5) |

---

## Current Active Development Tasks

- [ ] Set up monorepo structure: `/agent`, `/contracts`, `/frontend`, `/zkproof`
- [ ] Implement Libp2p peer discovery module (mDNS + Kademlia)
- [ ] Define Protobuf schemas: `DataOffer`, `PurchaseRequest`, `QualityAttestation`, `ApprovalEvent`
- [ ] Write Escrow smart contract (Hardhat + Solidity 0.8.x)
- [ ] Build ZK circuit for statistical quality attestation (circom or snarkjs)
- [ ] Implement local SLM data quality scorer
- [ ] Build seller-side human approval notification (desktop pop-up or CLI prompt)
- [ ] Build AES-256-GCM encrypt/decrypt pipeline for data payloads
- [ ] Create buyer and seller agent CLI with config file support
- [ ] Write integration test: full E2E buy/sell flow on local Hardhat network

---

## Related Files
- `PROJECT-detail.md` — full technical specification and architecture
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap and milestones
- `SECOND-KNOWLEDGE-BRAIN.md` — research papers, models, and self-update protocol
