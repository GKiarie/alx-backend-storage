#!/usr/bin/env python3
"""function that inserts a new document
in a collection based on kwargs
"""


def insert_school(mongo_collection, **kwargs):
    """insert new doc in collection"""
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id
