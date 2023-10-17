"""Python function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """returns all students sorted by average score
       args:
          mongo_collection: name of the collection
       return:
          list of students
    """
     return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
