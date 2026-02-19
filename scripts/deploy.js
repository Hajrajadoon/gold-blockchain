async function main() {
  const GoldAssetNFT = await ethers.getContractFactory("GoldAssetNFT");
  const goldAssetNFT = await GoldAssetNFT.deploy();

  await goldAssetNFT.deployed();
  console.log("GoldAssetNFT deployed to:", goldAssetNFT.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
