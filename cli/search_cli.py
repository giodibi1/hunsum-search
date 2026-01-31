import click
import random
import textwrap
from tabulate import tabulate
import adapters.search_backend.search_impl as search_impl


@click.group()
def search():
    pass


def wrap(text, width=50):
    return textwrap.fill(text, width=width)


@click.command()
@click.argument("text")
@click.option("-k", is_flag=True, help="Search by keyword")
def search_text(text, k):
    click.echo(f"Searching for text: {text}")
    out = search_impl.HunsumSearchImplementation().search(text)
    table = [
        [
            item.get("id"),
            wrap(item["title"], 40),
            wrap(item["url"], 60),
            item.get("date_of_creation"),
        ]
        for item in out
    ]

    click.echo(
        tabulate(
            table,
            headers=["ID", "Title", "URL", "Date of Creation"],
            tablefmt="fancy_grid",
        )
    )
    if k:
        click.echo("Searching by keyword")


def _generate_output() -> list[int]:
    n = 102  # Number of random numbers
    li = random.sample(range(1, 110), n)
    return li


@click.command()
def paging():
    li = _generate_output()
    page_size = 10
    page_total = (len(li) + page_size - 1) // page_size
    page_number = 1
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    page = li[start_index:end_index]
    click.echo(
        click.style(f"Page: {page_number} of {page_total}", fg="green", bold=True)
    )
    click.echo(f"Page {page_number}: {page}")

    while True:
        next_page = click.prompt(
            "n = next | p = previous | pagenumber | q = quit", type=str
        )
        if next_page.lower() == "n" and page_number < page_total:
            page_number += 1
        elif next_page.lower() == "p" and page_number > 1:
            page_number -= 1
            if page_number < 1:
                page_number = 1
        elif (
            next_page.isdigit() and int(next_page) <= page_total and int(next_page) >= 1
        ):
            page_number = int(next_page)
        elif next_page.lower() == "q":
            break
        else:
            continue

        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        page = li[start_index:end_index]

        click.clear()
        click.echo(
            click.style(f"Page: {page_number} of {page_total}", fg="green", bold=True)
        )
        click.echo(f"Page {page_number}: {page}")


search.add_command(search_text)
search.add_command(paging)
