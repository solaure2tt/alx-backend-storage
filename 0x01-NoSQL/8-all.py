#!/usr/bin/env python3
"""Python function that lists all documents in a collection"""
import pymongo


def list_all(mongo_collection):
    """ list all documents in a collection
        args:
          mongo_collection : name of the colection
        return:
          list of all documents in mongo_collection
    """
    if mongo_collection is not None:
        return mongo_collection.find()
