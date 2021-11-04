import json
import time
from collections import defaultdict

from src.csv_helper import write_to_csv_file
from web3 import Web3
from web3.contract import Contract


def merge_balance(a, b):
    for k, v in b.items():
        a[k] += v
    return a


class ERC20Helper:
    web3: Web3

    def __init__(self, web3: Web3):
        self.web3 = web3

    def __get_erc20_contract_from_address(self, contract_address: str) -> Contract:
        """
        validate ERC20 and return web3.Contract object from given contract address
        :param contract_address: address of the contract
        :return: web3.Contract
        """
        # TODO: for improvements i think we can use Etherscan API to get ABI of given contract.
        # TODO: read from file instead
        abi: json = json.loads(
            '[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')

        cs_contract = self.__get_checksum_address(contract_address)

        try:
            contract: Contract = self.web3.eth.contract(address=cs_contract, abi=abi)
            self.__validate_erc20(contract)
            return contract

        except ValueError as e:
            print(f"contract format is not correct: {e}")
            exit(1)

    def __get_checksum_address(self, address: str) -> str:
        """
        get checksum address and exit program if adresss formet is not correct
        :param address:
        :return: check sum address
        """
        try:
            check_sum_address = self.web3.toChecksumAddress(address)
            return check_sum_address
        except ValueError:
            print("address format is not correct")
            exit(1)

    @staticmethod
    def __validate_erc20(contract: Contract):
        """
        validate given contract by trying to call erc20 functions
        :param contract:
        """
        try:
            contract.functions.totalSupply().call()
            contract.functions.name().call()
            contract.functions.symbol().call()
            contract.functions.decimals().call()
        except Exception as e:
            print(f"address {contract.address} is not ERC20: {e}")
            exit(1)

    def get_contract_details(self, contract_address: str) -> None:
        """
        show detail of contract i.e. name, symbol, decimals, total supply
        :param contract_address: address of contract that want to get the detail
        """
        contract = self.__get_erc20_contract_from_address(contract_address)

        total_supply = contract.functions.totalSupply().call()
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()

        print(f"name: {name}")
        print(f"symbol: {symbol}")
        print(f"decimals: {decimals}")
        print(f"total supply: {total_supply} wei => {total_supply / 10 ** decimals}")

    def get_account_balance_from_address(self, contract_address: str, account: str) -> None:
        """
        show token balance that belonging to the account
        :param contract_address: address contract
        :param account: account to check the balance
        """
        contract = self.__get_erc20_contract_from_address(contract_address)
        cs_account = self.__get_checksum_address(account)

        symbol = contract.functions.symbol().call()
        balance = contract.functions.balanceOf(cs_account).call()
        decimals = contract.functions.decimals().call()

        print(f"Account: {account} has {balance / 10 ** decimals} of {symbol} ({balance} wei)")

    def holders(self, contract_address: str, n: int) -> None:
        """
        get top N holders of contract_address
        :param contract_address: address contract
        :param n: number of top holders
        """
        # TODO: check from event Transfer(address indexed from, address indexed to, uint256 value)
        # TODO: add cache for optimization
        contract = self.__get_erc20_contract_from_address(contract_address)

        latest_block = self.web3.eth.get_block_number()
        balances = self.get_transfer_event(contract, 0, latest_block)

        balance_list = [(k, int(v)) for k, v in balances.items()]
        print(sorted(balance_list, key=lambda x: x[1], reverse=True)[:n])

    def get_transfer_event(self, contract: Contract, from_block: int, to_block: int):
        try:
            total_block = to_block - from_block
            if total_block > 2000:
                raise Exception("block size is too big")
            print(f"from block {from_block} to {to_block} | size {total_block})")
            balances = defaultdict(lambda: 0)
            if from_block > to_block:
                return balances
            event_filter = contract.events.Transfer.createFilter(fromBlock=from_block, toBlock=to_block)
            events = event_filter.get_all_entries()
            print(f"transfer event: {len(events)}, from block {from_block} to {to_block}")
            if len(events) == 0:
                return balances
            for event in events:
                args = event['args']
                _from = args['from']
                _to = args['to']
                _value = int(args['value'])
                balances[_from] -= _value
                balances[_to] += _value

            return balances
        except Exception as e:
            # Infura query limit e.g. {'code': -32005, 'message': 'query returned more than 10000 results'}
            mid: int = (from_block + to_block) // 2
            print(f"result is too big: divine query to left({from_block}-{mid}) right {mid + 1}-{to_block}: {e}")
            left_block_result = self.get_transfer_event(contract, from_block, mid)
            right_block_result = self.get_transfer_event(contract, mid + 1, to_block)
            return merge_balance(left_block_result, right_block_result)

    def watch_tx(self, address, poll_interval=1):
        """
        connected to web socket and transactions of given address and print Etherscan URL
        :param address: address of contract
        :param poll_interval: interval of polling, default to 1 sec.
        """
        cs_address = self.__get_checksum_address(address)
        filtering = self.web3.eth.filter({
            'address': cs_address
        })
        try:
            while True:
                for tx in filtering.get_new_entries():
                    tx_hash_bytes = tx['transactionHash']
                    tx_hash = self.web3.toHex(tx_hash_bytes)
                    print(f'https://etherscan.io/tx/{tx_hash}')
                print(".")
                time.sleep(poll_interval)
        except KeyboardInterrupt:
            print('exit!')

    def get_tx_logs(self, contract_address, from_block, to_block):
        cs_address = self.__get_checksum_address(contract_address)
        print(f"getting tx from {from_block} to {to_block}")
        filtering = self.web3.eth.filter({
            'address': cs_address,
            'fromBlock': from_block,
            'toBlock': to_block
        })
        tx_list = filtering.get_all_entries()
        return tx_list

    def latest_transactions(self, contract_address: str, n: int):
        """
        query blockchain to get transaction of given contract address and number, display to CLI and save to files
        :param contract_address: address of the contract
        :param n: number of transaction
        """
        contract = self.__get_erc20_contract_from_address(contract_address)
        cs_address = self.__get_checksum_address(contract_address)

        # Get transaction from blockchain, there is limitation of infura, you can't query more than 10k record at the same time.
        number_of_tx = int(n)
        lastest_block_number = self.web3.eth.get_block_number()
        number_of_total_tx = 0
        windows = 128
        to_block = lastest_block_number
        total_logs = []
        while number_of_total_tx < number_of_tx:
            try:
                from_block = to_block - windows
                print(f'query from block {from_block} to {to_block} windows {windows}')
                logs = self.get_tx_logs(contract_address=cs_address, from_block=from_block, to_block=to_block)
                total_logs += logs
                number_of_total_tx = len(total_logs)
                to_block = from_block - 1
                print(f'total tx from this query {len(logs)}')
            except ValueError as e:
                # handle infura error
                print(e)
                windows = windows // 2  # if result is more than 10k record, try to query with smaller windows
                pass

        print(f'total tx: {len(total_logs)}')
        total_logs.sort(key=lambda tx: tx['blockNumber'], reverse=True)

        count_tx = 0
        output = []
        for tx in total_logs:
            if count_tx >= number_of_tx:
                break
            tx_hash_hex = tx['transactionHash']
            tx_hash = self.web3.toHex(tx_hash_hex)
            print(f'https://etherscan.io/tx/{tx_hash}')
            transaction = self.web3.eth.get_transaction(tx_hash)
            _from = transaction['from']
            _to = transaction['to']
            input = transaction['input']

            if not _to.lower() == contract_address.lower():
                # There are some tx that interact to others smart contract e.g. Uniswap deposit LP, etc.
                # I'm not sure that it's out of scope of the assignment or not ?
                # My idea is to get the contract abi from Ehterscan API and then I can decode function input by calling
                # contract.decode_function_input(input)
                continue
            count_tx += 1

            call_data = contract.decode_function_input(input)
            print(f"sender: {_from}")
            print(f"tx_hash: {tx_hash}")
            print(f"call data: {call_data}")
            output.append({"sender": _from, "tx_hash": tx_hash, "call_data": call_data})

        # write to file
        write_to_csv_file("latest_tx.csv", ['sender', 'tx_hash', 'call_data'], output)
