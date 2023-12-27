// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
}

contract TokenClaimContract {
    IERC20 public token;
    mapping(bytes32 => uint256) private eligibleAmounts;
    mapping(address => bool) private hasClaimed;
    bool private locked;

    modifier nonReentrant() {
        require(!locked, "No re-entrancy");
        locked = true;
        _;
        locked = false;
    }

    constructor(address _tokenAddress, address[] memory _addresses, uint256[] memory _amounts) {
        require(_addresses.length == _amounts.length, "Addresses and amounts length mismatch");
        token = IERC20(_tokenAddress);

        for (uint i = 0; i < _addresses.length; i++) {
            bytes32 hashedAddress = keccak256(abi.encodePacked(_addresses[i]));
            eligibleAmounts[hashedAddress] = _amounts[i];
        }
    }

    function claimTokens() public nonReentrant {
        require(!hasClaimed[msg.sender], "Tokens already claimed");

        bytes32 hashedCaller = keccak256(abi.encodePacked(msg.sender));
        uint256 amount = eligibleAmounts[hashedCaller];

        require(amount > 0, "No tokens available for claim");

        hasClaimed[msg.sender] = true;
        eligibleAmounts[hashedCaller] = 0;

        require(token.transfer(msg.sender, amount), "Token transfer failed");
    }

    // Additional functions as needed
}
