import requests


class EtherscanProxy:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_latest_txs(self, n: int, address: str) -> None:
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset={n}&sort=asc&apikey={self.api_key}"
        response = requests.get(url)
        json_response = response.json()

        print(json_response)


    def get_contract_abi(self, contract_address: str) -> str:
        url = f"""https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.api_key}"""
        response = requests.get(url)
        json_response = response.json()

        print(json_response)
