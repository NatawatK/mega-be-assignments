from typing import Optional

from web3 import Web3


class Web3Provider:

    @staticmethod
    def get_http_provider(http_endpoint: str) -> Optional[Web3]:
        try:
            w3 = Web3(Web3.HTTPProvider(http_endpoint))
            Web3Provider.check_connection(w3)
            return w3
        except Exception as e:
            print(f"cannot connect to HTTPProvider: {e}")
            return None

    @staticmethod
    def get_web_socket_provider(web_socket_endpoint: str) -> Optional[Web3]:
        try:
            w3 = Web3(Web3.WebsocketProvider(web_socket_endpoint))
            Web3Provider.check_connection(w3)
            return w3
        except Exception as e:
            print(f"cannot connect to WebsocketProvider: {e}")
            return None

    @staticmethod
    def check_connection(web3: Web3):
        if web3.isConnected():
            print("web3 is connected!")
            return web3
        else:
            raise ConnectionError("web3 is not connected!")