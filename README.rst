EssentialDB
===========

A Fast Embedded Database in Python.
------------------------------------

Use case: You want to prototype an idea wihtout a heavyweight database install. If the idea works out though, you don't want
to rewrite all of your data access code.

EssentialDB helps solve that problem by being (nearly) api compatible with MongoDB. That way when your idea starts to grow,
you can switch to MongoDB to scale.

* Syntax and semantics are very similar to MongoDB, lowering the barrier of entry.
* Fairly complex query support.
* Its in pure python.
* Its very fast.

Current Status
---------------
Just getting started!

Quickstart
-----------

Basic usage is straightforward::

    from essentialdb import EssentialDB
    #create or open the database
    author_db = EssentialDB(filepath="authors.db")
    #insert a document into the database
    author_db.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902});
    #find some entries
    results = author_db.find({"last':'Hughes'}
    #commit the changes to disk
    author_db.sync()

Or using the 'with' semantics to assure that write happen without having to explicitly call sync::

    with EssentialDB(filepath="authors.db") as author_db:
        author_db.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902});


Insert a document::

  author = {'first': 'Langston', 'last': 'Hughes', 'born': 1902}
  author_db.insert_one(author)

Insert many documents::

  authors = [{'first': 'Langston', 'last': 'Hughes', 'born': 1902},
             {'first': 'Ezra', 'last': 'Pound', 'born': 1885}]
  author_db.insert_many(authors)

Find one document::

  document = author_db.find_one({'first': 'Ezra', 'last': 'Pound'})

Find many::

  documents = author_db.find({'born': {'$gt': 1900}})

Update one::

  updated = author_db.update({'_id': {'$eq': "A345i"}}, {'born': 1902})

Update many::

  updated = author_db.update({'born': {'$gt': 1900}}, {'period': 'Modern'})

Remove Items::

  removed = author_db.remove({'period':'Modern'))

Write updates to disk::

  author_db.sync()

Queries
--------

Queries in EssentialDB follow the same basic form as MongoDB::

    { <field1>: { <operator1>: <value1> }, ... }



Comparison Query Selectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The $eq operator matches documents where the value of a field equals the specified value::

    authorDB.find({"born" : {"$eq": 1972}})

The $ne operator matches documents where the value of a field is not equal to the specified value::

    authorDB.find({"born" : {"$ne": 1972}})

The $gt operator matches documents where the value of a field is greater than the specified value::

    authorDB.find({"born" : {"$gt": 1900}})

The $gte operator matches documents where the value of a field is great than or equal to the specified value::

    authorDB.find({"born" : {"$gte": 1900}})

The $lt operator matches documents where the value of a field is less than the specified value::

    authorDB.find({"born" : {"$lt": 1900}})


The $lte operator matches documents where the value of a field is less than or equal to the specified value::

    authorDB.find({"born" : {"$lte": 1900}})

The $in operator matches documents where the value of a field is equal any item in the specified array::

    authorDB.find({"genre" : {"$in": ["tragedy", "drama"]}})

The $nin operator matches documents where the value of a field is not equal to any item in the specified array::

    authorDB.find({"genre" : {"$nin": ["tragedy", "drama"]}})


Boolean Operators
^^^^^^^^^^^^^^^^^
The $and operator matches documents where all the fields match::

    #find authors born after 1900 and before 2000
    author_db.find({'$and':[{'born': {'$gte': 1900}},{'born': {'$lt': 2000}}]})

The $or operator matches documents where any of the fields match::

    #find authors with either the first or last name John
    author_db.find({'$or':[{'first': {'$eg': 'John'}},{'last': {'$eq': 'John'}}]})

The $nor operator matches document where none of the conditions match::

    #find all authors who have neither the first or last name John
    author_db.find({"$nor":[{'first': {"$eq": 'John'}},{'last': {'$eq': 'John'}}]})


