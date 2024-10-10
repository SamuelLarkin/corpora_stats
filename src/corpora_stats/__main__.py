#!/usr/bin/env  python3

# from multiprocessing.pool import ThreadPool as Pool  # At least x2 slower.
from multiprocessing import Pool
from typing import Optional, Tuple

import click
from click_default_group import DefaultGroup

from corpora_stats.all_documents import AllDocuments
from corpora_stats.document import Document
from corpora_stats.utils import create_document, tabulate


@click.group(cls=DefaultGroup, default="wc", default_if_no_args=True)
def cli():
    pass


@cli.command()
@click.argument("files", nargs=-1)
@click.option(
    "-j",
    "--json",
    "do_json",
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help="output in json",
)
@click.option(
    "-f",
    "--format",
    "tablefmt",
    type=str,
    default="github",
    show_default=True,
    help="Table format (latex, github)",
)
@click.option(
    "-F",
    "--float",
    "floatfmt",
    type=str,
    default=".4f",
    show_default=True,
    help="float format",
)
@click.option(
    "-i",
    "--indent",
    "json_indent",
    type=int,
    default=None,
    show_default=True,
    help="json indentation",
)
def wc(
    files: Tuple[str],
    do_json: bool,
    tablefmt: str,
    floatfmt: str,
    json_indent: Optional[int],
):
    """
    Calculates minimum, maximum, sum, mean & sdev for bytes, chars, words &
    line per document and an overall for all documents.

    \b
    corpora-stats --json MY_CORPORA \\
    | head -n -1 \\
    | mlr --ijson --opprint --barred cat
    """
    if do_json:
        from json import encoder

        encoder.FLOAT_REPR = lambda o: format(o, floatfmt)

    overall: AllDocuments = AllDocuments()
    docs = []
    with Pool() as pool:
        for doc in pool.imap(create_document, files):
            overall += doc
            docs.append(doc)
            if do_json:
                print(doc.to_json(indent=json_indent))

    if do_json:
        print(overall.to_json(indent=json_indent))
    else:
        tabulate(docs, overall, tablefmt=tablefmt, floatfmt=floatfmt)


@cli.command("tabulate")
@click.argument("json_statistics", type=click.File(mode="rt"))
@click.option(
    "-f",
    "--format",
    "tablefmt",
    type=str,
    default="github",
    show_default=True,
    help="Table format (latex, github)",
)
@click.option(
    "-F",
    "--float",
    "floatfmt",
    type=str,
    default=".4f",
    show_default=True,
    help="float format",
)
def tabulate_cli(
    json_statistics,
    tablefmt: str,
    floatfmt: str,
):
    """
    Given a json file containing corpus statistics, tabulate the metrics.
    """
    from json import encoder

    encoder.FLOAT_REPR = lambda o: format(o, floatfmt)

    statistics = json_statistics.readlines()
    docs = [Document.from_json(data) for data in statistics[:-1]]
    all_docs = AllDocuments.from_json(statistics[-1])
    tabulate(docs, all_docs, tablefmt=tablefmt, floatfmt=floatfmt)


if __name__ == "__main__":
    cli()
