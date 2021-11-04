import os

import click
from dotenv import load_dotenv

from src.erc20helper import ERC20Helper
from src.web3_provider import Web3Provider

erc20helper: ERC20Helper


@click.group()
def cli():
    initialize()


@click.command()
@click.argument('contract_address')
def detail(contract_address):
    """Show name, symbol and decimals of the target contract_address"""
    erc20helper.get_contract_details(contract_address)
    pass


@click.command()
@click.argument('contract_address')
@click.argument('target_address')
def balance_of(contract_address, target_address):
    """Show the balance of target_address on the contract_address"""
    erc20helper.get_account_balance_from_address(contract_address, target_address)
    pass


@click.command()
@click.argument('contract_address')
def watch_tx(contract_address):
    """Subscribe Tx from contract_address"""
    erc20helper.watch_tx(contract_address)


@click.command()
@click.argument('n', type=int)
@click.argument('contract_address')
def latest_tx(n, contract_address):
    """Generate latest N transactions of contract_address"""
    erc20helper.latest_transactions(contract_address, n)


@click.command()
@click.argument('n', type=int)
@click.argument('contract_address')
def holders(n, contract_address):
    """Generate top N holder of contract_address to file"""
    erc20helper.holders(contract_address, n)


def initialize():
    global erc20helper
    load_dotenv()
    use_web_socket: int = int(os.getenv("USE_WEB_SOCKET", 0))

    if use_web_socket:
        web_socket_endpoint = os.getenv("WS_ENDPOINT", "")
        web3 = Web3Provider.get_web_socket_provider(web_socket_endpoint)
    else:
        http_endpoint = os.getenv("HTTP_ENDPOINT", "")
        web3 = Web3Provider.get_http_provider(http_endpoint)

    if web3 is None:
        print(f"cannot connect to web3, please check .env file")
        exit(1)
    erc20helper = ERC20Helper(web3)
    return erc20helper


if __name__ == '__main__':
    cli.add_command(detail)
    cli.add_command(holders)
    cli.add_command(latest_tx)
    cli.add_command(watch_tx)
    cli.add_command(balance_of)
    cli()
