// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GoldAssetNFT is ERC721, Ownable {

    uint256 public nextTokenId;

    struct GoldInfo {
        uint256 weightInGrams;
        uint256 purity; // e.g. 999
        string vaultId;
    }

    mapping(uint256 => GoldInfo) public goldDetails;

    constructor() ERC721("Tokenized Gold Asset", "TGA") {}

    function mintGoldAsset(
        address to,
        uint256 weightInGrams,
        uint256 purity,
        string calldata vaultId
    ) external onlyOwner {
        uint256 tokenId = nextTokenId++;
        _safeMint(to, tokenId);

        goldDetails[tokenId] = GoldInfo({
            weightInGrams: weightInGrams,
            purity: purity,
            vaultId: vaultId
        });
    }
}
