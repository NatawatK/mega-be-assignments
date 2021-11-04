import os

import click
from dotenv import load_dotenv

from src.erc20helper import ERC20Helper

erc20helper: ERC20Helper


@click.group()
def cli():
    initialize()
    pass


@click.command()
@click.argument('contract_address')
def detail(contract_address):
    erc20helper.get_contract_details(contract_address)
    pass


@click.command()
@click.argument('contract_address')
@click.argument('target_address')
def balance_of(contract_address, target_address):
    erc20helper.get_account_balance_from_address(contract_address, target_address)
    pass


@click.command()
@click.argument('contract_address')
def watch_tx(contract_address):
    erc20helper.watch_tx(contract_address)


@click.command()
@click.argument('n', type=int)
@click.argument('contract_address')
def latest_tx(n, contract_address):
    erc20helper.latest_transactions(contract_address, n)


@click.command()
@click.argument('N', type=int)
@click.argument('contract_address')
def holders():
    return


def initialize():
    global erc20helper
    load_dotenv()
    infura_project_id: str = os.getenv("INFURA_PROJECT_ID", "")
    if infura_project_id == '':
        raise RuntimeError("INFURA_PROJECT_ID is missing")
    erc20helper = ERC20Helper(infura_project_id)
    return erc20helper


if __name__ == '__main__':
    cli.add_command(detail)
    cli.add_command(holders)
    cli.add_command(latest_tx)
    cli.add_command(watch_tx)
    cli.add_command(balance_of)
    cli()
