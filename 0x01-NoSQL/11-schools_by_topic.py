#!/usr/bin/env python3
"""function that returns the list of
school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """ret list of schools with a topic"""
    query = {"topics": topic}
    result = mongo_collection.find(query)
    return list(result)
