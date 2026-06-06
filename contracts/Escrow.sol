// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract Escrow {
    using SafeERC20 for IERC20;

    struct Transaction {
        address buyer;
        address seller;
        uint256 amount;
        bool isLocked;
        bool isCompleted;
        uint256 lockTime;
    }

    IERC20 public token;
    mapping(string => Transaction) public transactions;
    
    event FundsLocked(string datasetId, address buyer, address seller, uint256 amount);
    event FundsReleased(string datasetId, address seller, uint256 amount);
    event FundsRefunded(string datasetId, address buyer, uint256 amount);

    constructor(address _token) {
        token = IERC20(_token);
    }

    function lockFunds(string memory datasetId, address seller, uint256 amount) external {
        require(transactions[datasetId].isLocked == false, "Funds already locked");
        
        token.safeTransferFrom(msg.sender, address(this), amount);
        
        transactions[datasetId] = Transaction({
            buyer: msg.sender,
            seller: seller,
            amount: amount,
            isLocked: true,
            isCompleted: false,
            lockTime: block.timestamp
        });
        
        emit FundsLocked(datasetId, msg.sender, seller, amount);
    }

    function confirmReceipt(string memory datasetId) external {
        Transaction storage tx = transactions[datasetId];
        require(msg.sender == tx.buyer, "Only buyer can confirm");
        require(tx.isLocked, "Funds not locked");
        require(!tx.isCompleted, "Already completed");

        tx.isCompleted = true;
        token.safeTransfer(tx.seller, tx.amount);
        
        emit FundsReleased(datasetId, tx.seller, tx.amount);
    }

    function refundBuyer(string memory datasetId) external {
        Transaction storage tx = transactions[datasetId];
        require(tx.isLocked, "Funds not locked");
        require(!tx.isCompleted, "Already completed");
        require(block.timestamp > tx.lockTime + 7 days, "Refund period not yet elapsed");

        tx.isLocked = false;
        token.safeTransfer(tx.buyer, tx.amount);
        
        emit FundsRefunded(datasetId, tx.buyer, tx.amount);
    }
}
