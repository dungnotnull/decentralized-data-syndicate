# Architecture Decision Records (ADRs) — decentralized-data-syndicate

## ADR-001: P2P Library Selection
**Status**: Accepted
**Date**: 2026-06-06

### Context
Need a P2P networking stack for buyer/seller agent discovery and direct data transfer.

### Decision
Use **js-libp2p** as the reference implementation, with Python agents communicating via a local JS bridge or REST proxy. py-libp2p is immature and not available on PyPI.

### Consequences
- Positive: Mature, well-tested, IPFS/Ethereum-proven stack
- Negative: Python agents need a JS sidecar or WebSocket bridge
- Alternative: Custom asyncio TCP protocol (rejected — too much bespoke code)

---

## ADR-002: ZK Proof Framework
**Status**: Accepted
**Date**: 2026-06-06

### Context
Need ZK proofs for data quality attestation without revealing raw data.

### Decision
Use **circom 2.0 + snarkjs (Groth16)** for circuit design, proof generation, and on-chain verifier export.

### Consequences
- Positive: Smallest proof size (~192 bytes), fastest verification, mature tooling
- Negative: Per-circuit trusted setup required; production needs proper ceremony
- Alternative: PLONK (universal setup, slightly larger proofs) — deferred to Phase 5 if needed

---

## ADR-003: L2 Chain Selection
**Status**: Accepted
**Date**: 2026-06-06

### Context
Escrow smart contracts need low gas fees and EVM compatibility.

### Decision
Use **Polygon PoS** as primary L2 target; **Arbitrum One** as secondary. Local development on Hardhat.

### Consequences
- Positive: Low gas, EVM compatible, good testnet faucet availability (Polygon Amoy)
- Negative: Polygon has centralized sequencer concerns; Arbitrum is more decentralized but slightly costlier

---

## ADR-004: Local SLM for Quality Scoring
**Status**: Accepted
**Date**: 2026-06-06

### Context
Need offline data quality assessment before ZK proof generation to avoid wasting compute.

### Decision**nUse **Ollama + Phi-3-mini-4k-instruct** as default local SLM. Fallback to Claude API if accuracy is insufficient.

### Consequences
- Positive: Fully offline, no API cost, fast enough on CPU
- Negative: Smaller model may miss subtle quality issues; prompt engineering critical

---

## ADR-005: Agent Implementation Language
**Status**: Accepted
**Date**: 2026-06-06

### Context
Need to choose primary backend language for buyer/seller agents.

### Decision
Use **Python 3.11** for agent logic, **Node.js** for blockchain scripts, **React + TypeScript** for frontend.

### Consequences
- Positive: Python has best ML ecosystem (transformers, sentence-transformers, PyCryptodome)
- Negative: Web3.py less mature than ethers.js; we bridge with Node.js scripts for contract deployment
