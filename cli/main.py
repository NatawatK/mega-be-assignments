import click
from cli.src.erc20helper import details


@click.group()
def cli():
    pass

@click.command()
@click.argument('contract_address')
def detail(contract_address):
    details(contract_address)
    # return

@click.command()
@click.argument('contract_address')
@click.argument('target_address')
def balance_of():
    return

@click.command()
@click.argument('contract_address')
def watch_tx():
    return

@click.command()
@click.argument('N')
@click.argument('contract_address')
def latest_tx():
    return

@click.command()
@click.argument('N')
@click.argument('contract_address')
def holders():
    return

if __name__ == '__main__':
    # TODO: load_env and check first
    cli.add_command(detail)
    cli.add_command(holders)
    cli.add_command(latest_tx)
    cli.add_command(watch_tx)
    cli.add_command(balance_of)
    cli()


