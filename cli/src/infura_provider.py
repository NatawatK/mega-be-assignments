from typing import Optional

from web3 import Web3


class InfuraProvider:

    @staticmethod
    def get_http_provider(infura_project_id: str) -> Optional[Web3]:
        infura_url = f'https://mainnet.infura.io/v3/{infura_project_id}'
        w3 = Web3(Web3.HTTPProvider(infura_url))
        return InfuraProvider.check_connection(w3)

    @staticmethod
    def get_web_socket_provider(infura_project_id: str) -> Web3:
        endpoint = f'wss://mainnet.infura.io/ws/v3/{infura_project_id}'
        w3 = Web3(Web3.WebsocketProvider(endpoint))
        return InfuraProvider.check_connection(w3)

    @staticmethod
    def check_connection(web3: Web3):
        if web3.isConnected():
            print("web3 is connected!")
            return web3
        else:
            raise ConnectionError("cannot connect to web3")