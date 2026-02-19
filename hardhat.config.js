import "@nomicfoundation/hardhat-toolbox";
import "dotenv/config";

export default {
  solidity: "0.8.20",
  networks: {
    cronosTestnet: {
      url: "https://evm-t3.cronos.org",
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};
