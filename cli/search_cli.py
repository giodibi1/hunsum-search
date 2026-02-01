import click
import random
import textwrap
from dateutil import parser
from tabulate import tabulate
import adapters.search_backend.search_impl as search_impl


@click.group()
def search():
    pass


def wrap(text, width=50):
    return textwrap.fill(text, width=width)


@click.command()
@click.argument("query")
@click.option("-page", help="Go to page number", type=int)
@click.option("-sort", multiple=True, help="Sort by field: 'field:[asc, desc]'")
@click.option(
    "-filter",
    multiple=True,
    help="Filter by keyword, date or range: 'keyword', 'date:[gt, gte, lt, lte]', 'date1:date2'",
)
def search_text(query, page, sort, filter):
    body = search_impl.HunsumSearchImplementation().search_body(query)
    hunsearch = search_impl.HunsumSearchImplementation()
    params: dict[str, any] = {
        "index": "test-index",
        "query": body,
        "size": 10,
        "from_": 0,
    }

    if page:
        params.update(hunsearch.param_page(page_number=page))

    if sort:
        try:
            params["sort"] = hunsearch.param_sort(list(sort))
        except search_impl.HunsumSearchInterface.SearchFormatException as e:
            raise click.ClickException(e.message)

    if filter:
        try:
            body["bool"][
                "filter"
            ] = search_impl.HunsumSearchImplementation().param_filter(filter=filter)
        except search_impl.HunsumSearchInterface.SearchFormatException as e:
            raise click.ClickException(e.message)

    out = hunsearch.search(params)

    if page and page > out["total"] // out["pageSize"] + 1:
        params.update(
            hunsearch.param_page(page_number=out["total"] // out["pageSize"] + 1)
        )
        out = hunsearch.search(params)

    table = [
        [
            item.get("id"),
            wrap(item["title"], 40),
            wrap(item["url"], 60),
            item.get("date_of_creation"),
        ]
        for item in out["hits"]
    ]

    click.echo(
        click.style(
            f"Page: {out['from'] // out['pageSize'] + 1} of {out['total'] // out['pageSize'] + 1}",
            fg="green",
            bold=True,
        )
    )
    click.echo(
        tabulate(
            table,
            headers=["ID", "Title", "URL", "Date of Creation"],
            tablefmt="fancy_grid",
        )
    )


@click.command()
@click.argument("name")
@click.option("-settings", help="Index settings", type=str)
def init_index(name, settings):
    search_impl.HunsumSearchImplementation().init_index(name, settings)
    click.echo(
        click.style(f"Index '{name}' initialized successfully.", fg="green", bold=True)
    )


search.add_command(search_text)
search.add_command(init_index)
