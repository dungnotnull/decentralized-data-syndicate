# Testnet Setup Guide

## Polygon Amoy Testnet

### RPC Endpoints
- https://rpc-amoy.polygon.technology
- https://polygon-amoy.blockpi.network/v1/rpc/public

### Faucets
- Official: https://faucet.polygon.technology/
- Alchemy: https://www.alchemy.com/faucets/polygon-amoy
- QuickNode: https://faucet.quicknode.com/polygon/amoy

### Test Wallets
Use Hardhat-generated wallets or MetaMask. Example test mnemonic (DO NOT USE IN PRODUCTION):

``nabandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
``n
### Chain Config
`yaml
chain_id: 80002
rpc_url: https://rpc-amoy.polygon.technology
explorer: https://amoy.polygonscan.com
``n
## Arbitrum Sepolia Testnet

### RPC Endpoints
- https://sepolia-rollup.arbitrum.io/rpc

### Faucets
- Official: https://sepolia.arbitrum.io/faucet
- Alchemy: https://www.alchemy.com/faucets/arbitrum-sepolia

### Chain Config
`yaml
chain_id: 421614
rpc_url: https://sepolia-rollup.arbitrum.io/rpc
explorer: https://sepolia.arbiscan.io
``n
## Local Hardhat Node
`ash
npx hardhat node --fork https://rpc-amoy.polygon.technology
``n
### Recommended: Run all Phase 1 integration tests on Hardhat before touching testnet.
