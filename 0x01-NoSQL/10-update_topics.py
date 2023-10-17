#!/usr/bin/env python3
""" Python function that changes all topics of
     a school document based on the name:
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """ update a document in a collection
        args:
          mongo_collection: name of the collection
          name:  school name to update
          topics: list of topics approached in the school
        return:
          nothing
    """
    myquery = { "name": name }
    newvalues = { "$set": { "topics": topics } }
    mongo_collection.update_many(myquery, newvalues)
