from web3 import Web3
import json
import requests
import csv

# Initialize a Web3 instance
web3 = Web3(Web3.HTTPProvider('https://XXXXXXXXXXXXXXXXXXXXXXX/'))

# Check if the connection is established
if web3.is_connected():
    print("Connected to Arbitrum")
else:
    print("Failed to connect to Arbitrum")

def get_abi_from_arbiscan(contract_address, arbiscan_api_key):
    url = f"https://api.arbiscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={arbiscan_api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        if result['status'] == '1':
            abi = result['result']
            return abi
        else:
            print(f"Failed to retrieve ABI: {result['result']}")
            return None
    else:
        print(f"HTTP Error: {response.status_code}")
        return None

arbiscan_api_key = "XXXXXXXXXXXXXXXXXXXXXXX"
contract_address = Web3.to_checksum_address("XXXXXXXXXXXXXXXXXXXXXXX")
contract_abi = get_abi_from_arbiscan(contract_address, arbiscan_api_key)

# Check if the ABI was retrieved
if contract_abi:
    # Convert the ABI string to a JSON object
    abi_json = json.loads(contract_abi)

    # Save the ABI in JSON format
    with open('./contract_abi.json', 'w') as abi_file:
        json.dump(abi_json, abi_file, indent=4)

    print("ABI saved as a JSON file.")
else:
    print("Unable to retrieve or save the ABI.")

# Create an instance of the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Read addresses from the CSV file
addresses = []
with open('addresses.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header if your file has one
    for row in csv_reader:
        addresses.append(row[0])  # Ensure addresses are in the first column

# Retrieve balances for each address
balances = {}
i = 0
for address in addresses:
    balance = contract.functions.getBalance(Web3.to_checksum_address(address)).call()
    balances[address] = balance * 10**-18
    print(i)
    i += 1

# Display the results
for address, balance in balances.items():
    print(f"{address}, {balance}")
