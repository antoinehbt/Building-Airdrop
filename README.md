** Contract.sol **

This Solidity contract allows users to claim pre-determined token amounts from a specified ERC20 token contract. It uses a non-reentrant modifier to prevent reentrancy attacks and a mapping of hashed addresses to control eligibility and claim status. The claimTokens function enables eligible users to claim their tokens once, based on the initial configuration set in the constructor. This is not the final version of the code but a test version that does not expect the addresses included in the arguments to be hashed.

** Stakers.py **

This script verifies stakeholders positions in an Arbitrum contract using Web3.py. It reads a list of addresses from a CSV file and queries the contract for the balance associated with each address. The script outputs these balances to the console.

** Traders.py **

This script scrapes a trader leaderboard from a dashboard using Selenium. This data comes from a perpetual DEX on Arbitrum. It processes the raw scraped data into structured information by creating a DataFrame with Pandas, formatting and converting the data for numerical analysis.