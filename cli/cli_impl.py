import click


@click.command()
@click.option("--name", prompt="Mi a neved?")
def hello(name):
    click.echo(f"Szia, {name}!")


if __name__ == "__main__":
    hello()
