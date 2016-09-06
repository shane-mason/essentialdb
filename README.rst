EssentialDB
===========

A Fast Embedded Database in Python.
------------------------------------

EssentialDB attempts to solve a common use case: you want a very simple data access mechanism without a heavyweight install.

* Syntax and semantics are very similar to Mongo, lowering the barrier of entry.
* Fairly complex query support.
* Its in pure python.
* Its very fast.

Current Status
---------------
Just getting started!

Quickstart
-----------

Create a database::

  from essentialdb import EssentialDB, SimpleCollection
  authorDB = EssentialDB(collection=SimpleCollection(), filepath="authors.db")

Create a database using with::

  with EssentialDB(collection=SimpleCollection(), filepath="authors.db") as authorsDB:
    #perform database operations here
    pass

  #database is closed and synced here

Insert a document::

  author = {'first': 'Langston', 'last': 'Hughes', 'born': 1902}
  authorDB.insert_one(author)

Insert many documents::

  authors = [{'first': 'Langston', 'last': 'Hughes', 'born': 1902},
             {'first': 'Ezra', 'last': 'Pound', 'born': 1885}]
  authorDB.insert_many(authors)

Find one document::

  document = authorDB.find_one({'first': 'Ezra', 'last': 'Pound'})

Find many::

  documents = authorDB.find({'born': {'$gt': 1900}})

Update one::

  updated = authorDB.update({'_id': {'$eq': "A345i"}}, {'born': 1902})

Update many::

  updated = authorDB.update({'born': {'$gt': 1900}}, {'period': 'Modern'})

Remove Items::

  removed = authorDB.remove({'period':'Modern'))

Write updates to disk::

  authorDB.sync()

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

The $gte operator matches documents where the value of a field is great than or equal to the specified value:

    authorDB.find({"born" : {"$gte": 1900}})

The $lt operator matches documents where the value of a field is less than the specified value::

    authorDB.find({"born" : {"$lt": 1900}})


The $lte operator matches documents where the value of a field is less than or equal to the specified value::

    authorDB.find({"born" : {"$lte": 1900}})

The $in operator matches documents where the value of a field is equal any item in the specified array::

    authorDB.find({"genre" : {"$in": ["tragedy", "drama"]}})

The $nin operator matches documents where the value of a field is not equal to any item in the specified array::

    authorDB.find({"genre" : {"$nin": ["tragedy", "drama"]}})
