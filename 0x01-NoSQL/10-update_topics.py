#!/usr/bin/env python3
"""function that changes all topics of a
school document based on the name
"""


def update_topics(mongo_collection, name, topics):
    """change topics of a doc based on a name"""
    query = {"name": name}
    new_values = {"$set": {"topics": topics}}
    result = mongo_collection.update_many(query, new_values)
    return result.modified_count
