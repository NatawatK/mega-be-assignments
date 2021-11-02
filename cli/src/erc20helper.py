import os
from typing import Optional
from web3 import Web3

from dotenv import load_dotenv
import json

from web3.contract import Contract
from src.addresses import *


# TODO: convert to class
def init_dotenv():
    load_dotenv()

    infura = os.getenv("INFURA_PROJECT_ID", "INFURA_PROJECT_ID")
    print(infura)
    return {"INFURA_PROJECT_ID": infura}



def getProvider(url: str) -> Optional[Web3]:
    w3 = Web3(Web3.HTTPProvider(url))

    print(w3.isConnected())
    if w3.isConnected():
        return w3
    else: 
        exit(1)
        return None


def main():
    env = load_dotenv()
    infura_project_id = os.getenv("INFURA_PROJECT_ID", "INFURA_PROJECT_ID")
    infura_url = f'https://mainnet.infura.io/v3/{infura_project_id}'
    print(infura_url)
    web3 = getProvider(infura_url)
    print(web3.eth.get_block_number())


    get_contract_from_address(web3, '0xcd5dc768fe61e5702ad88f3bb34ced5a30fc1b49')
    
    # latest_transactions(web3, alpha, 10)

    get_account_balance_from_address(web3, address=usdt, account='0xcd5dc768fe61e5702ad88f3bb34ced5a30fc1b49')



def get_contract_from_address(web3: Web3, contract_address: str) -> Contract:
    # TODO: read from file instead
    abi: json = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

    if web3.isChecksumAddress(contract_address):
        check_sum_adrress = contract_address
    else:
        check_sum_adrress = web3.toChecksumAddress(contract_address)

    print(contract_address)
    print(check_sum_adrress)
    print(web3.toChecksumAddress(contract_address)) # always check sum is fine

    contract: Contract = web3.eth.contract(address=check_sum_adrress, abi=abi)
    return contract


def get_account_balance_from_address(web3, contract_address, account):
    ## Balance of
    contract = get_contract_from_address(web3, contract_address)
    print(f'account {account}')
    print(f'account checkssum {web3.toChecksumAddress(account)}')
    print(contract.functions.name().call())
    print(contract.functions.symbol().call())
    balance = contract.functions.balanceOf(web3.toChecksumAddress(account)).call()
    print(web3.fromWei(balance, 'ether'))


def get_contract_details(web3, address):
    ## Details
    cs_addr = web3.toChecksumAddress(address)
    contract = web3.eth.contract(address=cs_addr, abi=abi)
    totalSupply = contract.functions.totalSupply().call()
    name = contract.functions.name().call()
    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()
    print(f"name: {name}")
    print(f"symbol: {symbol}")
    print(f"decimals: {decimals}")



def holders(web3, address, n): 
    pass
    # TODO: check from event Transfer(address indexed from, address indexed to, uint256 value)
    # TODO: add cache for optimzation
    # print(web3.eth.get_logs)


def watch_tx(web3, address):
    pass
   ## watch tx = web_socket



def latest_transactions(web3, address: str, n: int):
    contract = get_contract_from_address(web3, address)
    cs_addr = web3.toChecksumAddress(address)
   ## latest tx N = filter by address
   # (<Function transfer(address,uint256)>, {'_to': '0xB3f923eaBAF178fC1BD8E13902FC5C61D3DdEF5B', '_value': 61396000000000000000000})

    block_number = web3.eth.get_block_number()

    N = 10

    filter = web3.eth.filter({
        'address': cs_addr,
        'fromBlock': block_number-N,
        'toBlock': 'latest'
    })

    logs = web3.eth.get_filter_logs(filter.filter_id)

    print(len(logs))
    tx_hash = logs[0]['transactionHash']

    transaction = web3.eth.get_transaction(tx_hash)
    print(transaction.input)

    print(input)
    print(contract.decode_function_input(transaction.input))



if __name__ == '__main__':
    main()
