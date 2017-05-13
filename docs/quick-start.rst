
Quickstart
-----------

Install with pip::

    pip install essentialdb


Basic usage is straightforward::

    from essentialdb import EssentialDB

    #create or open the database
    db = EssentialDB(filepath="my.db")

    #get the collection
    authors = db.get_collection('authors')

    #insert a document into the collection
    authors.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902});

    #find some entries
    results = authors.find({'last':'Hughes'})

    #commit the changes to disk
    db.sync()

Or using the 'with' semantics to assure that write happen without having to explicitly call sync::

    with EssentialDB("my.db").get_collection('authors') as author_db:
        author_db.insert_one({'first': 'Langston', 'last': 'Hughes', 'born': 1902})


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

Note that updating fields that don't currently exist in the document will add the field to the document.

Remove Items::

  removed = author_db.remove({'period':'Modern'})

Nested Queries::

    customer_db.insert_one({'first': 'John', 'last': 'Smith', 'address': { 'street': '10 Maple St', 'city': 'Missoula', 'state': 'MT'}})
    results = customer_db.find({'address.state':'MT'})

Note that nested query support means that key names can not include a period.

Write updates to disk::

    author_db.sync()


