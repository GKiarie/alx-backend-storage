#!/usr/bin/env python3
"""function that lists all documents in a collection"""


def list_all(mongo_collection):
    """list all docs in a collection"""
    if mongo_collection is None:
        return []
    documents = list(mongo_collection.find({}))
    return documents
