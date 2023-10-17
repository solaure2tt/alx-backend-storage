#!/usr/bin/env python3
"""Python function that returns the list of school having a specific topic"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """ returns the list of school having a specific topic
        args:
          mongo_collection: name of the collection
          topic: topic searched
        return:
          the document which have the specifed topic
    """
    return mongo_collection.find({"topics": topic})
