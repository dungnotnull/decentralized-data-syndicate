# Decentralized Data Syndicate

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Solidity ^0.8.20](https://img.shields.io/badge/solidity-^0.8.20-green.svg)

**Decentralized Data la Syndicate** is a trustless, AI-driven marketplace for high-quality datasets. It leverages **ZK-SNARKs** for quality attestation and **Symmetric Encryption** for secure delivery, allowing buyers to find data via natural language and sellers to monetize assets without compromising privacy.

---

## Core Architecture

### The Three Pillars
1. **AI Agent Layer**: Uses SLMs (Phi-3) and LLMs (Claude/GPT-4) to translate natural language "needs" into technical specifications.
2. **ZK-Quality Layer**: Circom circuits generate proofs that a dataset meets specific criteria (row count, null rates) without revealing the data.
3. **Blockchain Escrow**: A Solidity-based escrow ensures funds are only released once the buyer confirms receipt of valid data.

### Technical Stack
- **Language**: Python 3.11+ | Solidity ^0.8.20
- **P2P Network**: Libp2p-inspired Asyncio GossipSub
- **ZK Proofs**: Circom 2.0 -> SnarkJS -> Solidity Verifier
- **Encryption**: X25519 (Key Exchange) + AES-256-GCM (Payload)
- **AI/ML**: Ollama (Local SLM) -> BGE-Small (Embeddings)

---

## Workflow

### 1. Discovery
- **Buyer**: "I need 10k health records with < 5% nulls in the age column."
- **Agent**: Translates this into a `DataNeedSpec` Protobuf message and broadcasts it to the P2P network.

### 2. Attestation
- **Seller**: Matches the need against their local catalog.
- **ZK-Proof**: Generates a proof that the dataset matches the `min_rows` and `max_null_rate` requirements.
- **Offer**: Broadcasts a `DataOffer` containing the ZK-proof and a price.

### 3. Transaction
- **Escrow**: Buyer locks USDC in the `Escrow.sol` contract.
- **Transfer**: Seller and Buyer perform an ECDH key exchange; data is streamed encrypted via P2P.
- **Settlement**: Buyer confirms receipt; Escrow releases funds to the Seller.

---

## Getting Started

### Prerequisites
- Ollama (for local SLM)
- Hardhat (for local blockchain)
- Circom (for ZK circuits)

### Installation
```bash
git clone https://github.com/dungnotnull/decentralized-data-syndicate.git
cd decentralized-data-syndicate
cp .env.example .env
pip install -r requirements.txt
```

### Running the MVP
```bash
# 1. Start Hardhat node
npx hardhat node

# 2. Start Seller Agent
python agent/src/seller_agent.py

# 3. Start Buyer Agent
python agent/src/buyer_agent.py
```

---

## Project Structure
```text
??? agent/            # AI Agents & P2P Logic
?   ??? proto/        # Protobuf Message Definitions
?   ??? src/          # Buyer, Seller, & Crypto implementation
??? contracts/        # Solidity Escrow & Token contracts
??? zkproof/          # Circom circuits & Proof generation
??? docs/             # Architecture Decision Records (ADRs)
??? .env              # Environment variables
```

## License
MIT License. See LICENSE for details.
