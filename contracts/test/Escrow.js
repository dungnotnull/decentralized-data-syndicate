const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('Escrow', function () {
  let Escrow, MockToken, escrow, token;
  let owner, buyer, seller;
  const datasetId = ethers.encodeBytes32String('ds-001');
  const amount = ethers.parseUnits('100', 6);

  beforeEach(async function () {
    [owner, buyer, seller] = await ethers.getSigners();

    const MockTokenFactory = await ethers.getContractFactory('MockToken');
    token = await MockTokenFactory.deploy();
    await token.waitForDeployment();

    const EscrowFactory = await ethers.getContractFactory('Escrow');
    escrow = await EscrowFactory.deploy(await token.getAddress());
    await escrow.waitForDeployment();

    await token.mint(buyer.address, amount);
    await token.connect(buyer).approve(await escrow.getAddress(), amount);
  });

  it('Should lock funds and emit event', async function () {
    await expect(
      escrow.connect(buyer).lockFunds(datasetId, seller.address, amount)
    )
      .to.emit(escrow, 'FundsLocked')
      .withArgs(datasetId, buyer.address, seller.address, amount);

    const deal = await escrow.deals(datasetId);
    expect(deal.buyer).to.equal(buyer.address);
    expect(deal.seller).to.equal(seller.address);
    expect(deal.amount).to.equal(amount);
    expect(deal.state).to.equal(1);
  });

  it('Should release funds on buyer confirmation', async function () {
    await escrow.connect(buyer).lockFunds(datasetId, seller.address, amount);

    await expect(
      escrow.connect(buyer).confirmReceipt(datasetId)
    )
      .to.emit(escrow, 'FundsReleased')
      .withArgs(datasetId, seller.address, amount);

    const deal = await escrow.deals(datasetId);
    expect(deal.state).to.equal(2);
    expect(await token.balanceOf(seller.address)).to.equal(amount);
  });

  it('Should refund after timeout', async function () {
    await escrow.connect(buyer).lockFunds(datasetId, seller.address, amount);

    await ethers.provider.send('evm_increaseTime', [73 * 60 * 60]);
    await ethers.provider.send('evm_mine');

    await expect(
      escrow.connect(seller).refundBuyer(datasetId)
    )
      .to.emit(escrow, 'FundsRefunded')
      .withArgs(datasetId, buyer.address, amount);

    const deal = await escrow.deals(datasetId);
    expect(deal.state).to.equal(3);
  });
});
