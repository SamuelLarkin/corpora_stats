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
):
    """
    Helpers function to tabulate.
    """
    data = {
        "line": [doc.line for doc in docs],
        "filename": [doc.filename for doc in docs],
    }
    doc_dicts = [doc.to_dict() for doc in docs]
    for unit in ("byte", "char", "word"):
        for metric in ("sum", "min", "max", "mean", "sdev"):
            data[f"{unit}_{metric}"] = [doc[unit][metric] for doc in doc_dicts]

    print(tabulate_ext(data, headers=data.keys(), tablefmt=tablefmt), "\n")

    all_docs = overall.to_dict()
    data = [[k] + list(v.values()) for k, v in all_docs.items()]
    print(
        tabulate_ext(
            data,
            headers=["OVERALL"] + list(all_docs["bytes"].keys()),
            floatfmt=floatfmt,
            tablefmt=tablefmt,
        )
    )
