// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Escrow {
    enum State { IDLE, LOCKED, RELEASED, REFUNDED }

    struct Deal {
        address buyer;
        address seller;
        uint256 amount;
        bytes32 datasetId;
        State state;
        uint256 lockTime;
    }

    mapping(bytes32 => Deal) public deals;
    IERC20 public token;
    uint256 public constant REFUND_DELAY = 72 hours;

    event FundsLocked(bytes32 indexed datasetId, address indexed buyer, address indexed seller, uint256 amount);
    event FundsReleased(bytes32 indexed datasetId, address indexed seller, uint256 amount);
    event FundsRefunded(bytes32 indexed datasetId, address indexed buyer, uint256 amount);

    constructor(address _token) {
        token = IERC20(_token);
    }

    function lockFunds(bytes32 datasetId, address seller, uint256 amount) external {
        require(deals[datasetId].state == State.IDLE, "Deal already exists");
        require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        deals[datasetId] = Deal({
            buyer: msg.sender,
            seller: seller,
            amount: amount,
            datasetId: datasetId,
            state: State.LOCKED,
            lockTime: block.timestamp
        });
        emit FundsLocked(datasetId, msg.sender, seller, amount);
    }

    function confirmReceipt(bytes32 datasetId) external {
        Deal storage deal = deals[datasetId];
        require(deal.buyer == msg.sender, "Only buyer can confirm");
        require(deal.state == State.LOCKED, "Not locked");
        deal.state = State.RELEASED;
        require(token.transfer(deal.seller, deal.amount), "Release failed");
        emit FundsReleased(datasetId, deal.seller, deal.amount);
    }

    function refundBuyer(bytes32 datasetId) external {
        Deal storage deal = deals[datasetId];
        require(deal.state == State.LOCKED, "Not locked");
        require(block.timestamp >= deal.lockTime + REFUND_DELAY, "Refund window not elapsed");
        deal.state = State.REFUNDED;
        require(token.transfer(deal.buyer, deal.amount), "Refund failed");
        emit FundsRefunded(datasetId, deal.buyer, deal.amount);
    }
}
