EssentialDB
============

|CI Status| |Cov Status| For Python 3.4, 3.5, 3.6 & 3.7(Nightly)

EssentialDB is a pure Python document database developed to meet the following tenets:

1. Databases shouldn't slow down development - a developer should be able to integrate a database in less than a minute.
2. Development databases should have a complete feature set and be performant enough for prototyping and project startups
3. Development databases should provide a path to scale when your project takes off

`Project On GitHub <https://github.com/shane-mason/essentialdb>`_ |
`Full Docs @ ReadTheDocs <http://essentialdb.readthedocs.io/en/latest/>`_ |
`Distribution On Pypi <https://pypi.python.org/pypi/essentialdb>`_

Speeding Development
----------------------

Our first tenet is that you should be able to start developing in less than a minute. Since EssentialDB is an 'embedded' database, there is no external services or dependencies to install or administrate. The tenet here is to take you from concept to development in less than a minute.
Install with pip::

    pip install essentialdb


Basic usage is straightforward::

    from essentialdb import EssentialDB

    #create or open the database
    db = EssentialDB(filepath="my.db")

    #get the collection
    authors = db.get_collection('authors')

    #use the abbreviated syntax
    books = db.books

    #insert a document into the collection
    authors.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902});

    #find some entries
    results = authors.find({'last':'Hughes'})

    #commit the changes to disk
    db.sync()

Or using the 'with' semantics to assure that write happen without having to explicitly call sync::

    with db.authors as author_collection:
        author_collection.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902})


Insert a document::

  author = {'first': 'Langston', 'last': 'Hughes', 'born': 1902}
  author_collection.insert_one(author)

Insert many documents::

  authors = [{'first': 'Langston', 'last': 'Hughes', 'born': 1902},
             {'first': 'Ezra', 'last': 'Pound', 'born': 1885}]
  author_collection.insert_many(authors)

Find one document::

  document = author_collection.find_one({'first': 'Ezra', 'last': 'Pound'})

Find many::

  documents = author_collection.find({'born': {'$gt': 1900}})

Update one::

  updated = author_collection.update({'_id': {'$eq': "A345i"}}, {'born': 1902})

Update many::

  updated = author_collection.update({'born': {'$gt': 1900}}, {'period': 'Modern'})

Note that updating fields that don't currently exist in the document will add the field to the document.

Remove Items::

  removed = author_collection.remove({'period':'Modern'})

Nested Queries::

    customer_collection.insert_one({'first': 'John', 'last': 'Smith', 'address': { 'street': '10 Maple St', 'city': 'Missoula', 'state': 'MT'}})
    results = customer_db.find({'address.state':'MT'})

Note that nested query support means that key names can not include a period.

Write updates to disk::

    author_collection.sync()



Features & Performance
-----------------------

Our second tenet is that EssentialDB should have the performance and features you need to get your project rolling.

EssentialDB supports a very rich queries that follow the same basic form as MongoDB::

    { <field1>:  <operator1>: <value1> }, ... }

Most comparison operators are supported, including equals, not equals,  less than, greater than::

    author_collection.find({"born" : {"$gt": 1900}})


You can even test against lists of items using $in and $nin::

    author_collection.find({"genre" : {"$in": ["tragedy", "drama"]}})

AND and OR boolean operators allow you to make arbitrarily complex queries::

    #find authors born after 1900 and before 2000
    author_collection.find({'$and':[{'born': {'$gte': 1900}},{'born': {'$lt': 2000}}]})

    #find authors with either the first or last name John
    author_collection.find({'$or':[{'first': {'$eg': 'John'}},{'last': {'$eq': 'John'}}]})

We've tested EssentialDB under some typical use cases, and seen that it is plenty performant for many use cases with small to moderate loads.

Where is it used?
-----------------
EssentialDB is being used in a variety of small projects. Most notably, it is powering some of the features behind kinder.farm_.

.. |CI Status| image:: https://travis-ci.org/shane-mason/essentialdb.svg?branch=master
   :target: https://travis-ci.org/shane-mason/essentialdb

.. |Cov Status| image:: https://coveralls.io/repos/github/shane-mason/essentialdb/badge.svg?branch=master
   :target: https://coveralls.io/github/shane-mason/essentialdb?branch=master

.. _kinder.farm: https://kinder.farm
