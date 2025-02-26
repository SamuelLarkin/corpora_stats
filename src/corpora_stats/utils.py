from typing import List

from tabulate import tabulate as tabulate_ext
from xopen import xopen

from corpora_stats.all_documents import AllDocuments
from corpora_stats.document import Document


def create_document(filename: str) -> Document:
    """
    Helper function to process documents in parallel.
    """
    with xopen(filename, mode="rb") as cin:
        doc = Document(filename)
        for line in cin:
            doc.update(line)

    return doc


def tabulate(
    docs: List[Document],
    overall: AllDocuments,
    tablefmt="github",
    floatfmt=".4f",
    do_extra_metrics: bool = False,
):
    """
    Helpers function to tabulate.
    """
    metrics = (
        ("count", "min", "max", "mean", "sdev") if do_extra_metrics else ("count",)
    )
    data = {
        "line": [doc.line for doc in docs],
        "filename": [doc.filename for doc in docs],
    }
    doc_dicts = [doc.to_dict() for doc in docs]
    for unit in ("byte", "char", "word"):
        if do_extra_metrics:
            for metric in metrics:
                data[f"{unit}_{metric}"] = [doc[unit][metric] for doc in doc_dicts]
        else:
            data[f"{unit}"] = [doc[unit]["count"] for doc in doc_dicts]

    print(tabulate_ext(data, headers=list(data.keys()), tablefmt=tablefmt), "\n")

    all_docs = overall.to_dict()
    footer_data = [
        [filename] + [document[metric] for metric in metrics]
        for filename, document in all_docs.items()
    ]
    print(
        tabulate_ext(
            footer_data,
            headers=["OVERALL"] + list(metrics),
            floatfmt=floatfmt,
            tablefmt=tablefmt,
        )
    )
