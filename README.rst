EssentialDB
============

EssentialDB is a pure Python document database developed to meet the following tenets:

1. Databases shouldn't slow down development - a developer should be able to integrate a database in less than a minute.
2. Development databases should have a complete feature set and be performant enough for prototyping and project startups
3. Development databases should provide a path to scale when your project takes off

`Project On GitHub <https://github.com/shane-mason/essentialdb>`_ |
`Full Docs @ ReadTheDocs <http://essentialdb.readthedocs.io/en/latest/>`_ |
`Distribution On Pypi <https://pypi.python.org/pypi/essentialdb>`_

Speeding Development
---------------------

Our first tenet is that you should be able to start developing in less than a minute. Since EssentialDB is an 'embedded' database, there is no external services or dependencies to install or administrate. The tenet here is to take you from concept to development in less than a minute.

Installing is this simple::

    pip install essentialdb


Using is this simple::

    from essentialdb import EssentialDB

    #create or open the database
    author_db = EssentialDB(filepath="authors.db")

    #insert a document into the database
    author_db.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902});

    #create an index on last names
    author_db.createIndex({'last': "hashed"})

    #find some entries
    results = author_db.find({'last':'Hughes'}

    #commit the changes to disk
    author_db.sync()


Documents are just Python dictionaries and EssentialDB provides an API to easily store and retrieve them.

Features & Performance
-----------------------

Our second tenet is that EssentialDB should have the performance and features you need to get your project rolling.

EssentialDB supports a very rich queries that follow the same basic form as MongoDB::

    { <field1>:  <operator1>: <value1> }, ... }

Most comparrison operators are supported, including equals, not equals,  less than, greater than::

    author_db.find({"born" : {"$gt": 1900}})


You can even test against lists of items using $in and $nin::

    author_db.find({"genre" : {"$in": ["tragedy", "drama"]}})

AND and OR boolean operators allow you to make arbitrarily complex queries::

    #find authors born after 1900 and before 2000
    author_db.find({'$and':[{'born': {'$gte': 1900}},{'born': {'$lt': 2000}}]})

    #find authors with either the first or last name John
    author_db.find({'$or':[{'first': {'$eg': 'John'}},{'last': {'$eq': 'John'}}]})


We've tested EssentialDB under some typical use cases, and seen that it is plenty performant for many use cases with small to moderate loads.

