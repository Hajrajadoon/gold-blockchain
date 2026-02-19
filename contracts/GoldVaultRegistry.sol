// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract GoldVaultRegistry is Ownable {

    struct Vault {
        string name;
        string location;
        bool active;
    }

    mapping(string => Vault) public vaults;

    function registerVault(
        string calldata vaultId,
        string calldata name,
        string calldata location
    ) external onlyOwner {
        vaults[vaultId] = Vault({
            name: name,
            location: location,
            active: true
        });
    }

    function deactivateVault(string calldata vaultId) external onlyOwner {
        vaults[vaultId].active = false;
    }

    function isVaultActive(string calldata vaultId) external view returns (bool) {
        return vaults[vaultId].active;
    }
}
