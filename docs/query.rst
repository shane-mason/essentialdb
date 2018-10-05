
Queries
========

Queries in EssentialDB follow the same basic form as MongoDB::

    { <field1>: { <operator1>: <value1> }, ... }


Comparison Query Selectors
---------------------------

The $eq operator matches documents where the value of a field equals the specified value::

    author_collection.find({"born" : {"$eq": 1972}})

The $ne operator matches documents where the value of a field is not equal to the specified value::

    author_collection.find({"born" : {"$ne": 1972}})

The $gt operator matches documents where the value of a field is greater than the specified value::

    author_collection.find({"born" : {"$gt": 1900}})

The $gte operator matches documents where the value of a field is great than or equal to the specified value::

    author_collection.find({"born" : {"$gte": 1900}})

The $lt operator matches documents where the value of a field is less than the specified value::

    author_collection.find({"born" : {"$lt": 1900}})


The $lte operator matches documents where the value of a field is less than or equal to the specified value::

    author_collection.find({"born" : {"$lte": 1900}})

The $in operator matches documents where the value of a field is equal any item in the specified array::

    author_collection.find({"genre" : {"$in": ["tragedy", "drama"]}})

The $nin operator matches documents where the value of a field is not equal to any item in the specified array::

    author_collection.find({"genre" : {"$nin": ["tragedy", "drama"]}})


Boolean Operators
------------------
The $and operator matches documents where all the fields match::

    #find authors born after 1900 and before 2000
    author_collection.find({'$and':[{'born': {'$gte': 1900}},{'born': {'$lt': 2000}}]})

The $or operator matches documents where any of the fields match::

    #find authors with either the first or last name John
    author_collection.find({'$or':[{'first': {'$eq': 'John'}},{'last': {'$eq': 'John'}}]})

The $nor operator matches document where none of the conditions match::

    #find all authors who have neither the first or last name John
    author_collection.find({"$nor":[{'first': {"$eq": 'John'}},{'last': {'$eq': 'John'}}]})



