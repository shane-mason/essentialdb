
EssentialDB Documentation
=========================

.. toctree::
   :maxdepth: 2

   quick-start
   query
   serializers
   performance
   api


.. include:: ../README.rst


Changelog:
* 0.5 - 01.07.2017 - Several changes, including::
      - Added thread lock for inserts, updates and disk writes
      - Refactored serialization into PickSerializer class
      - Added JSONSerializer class
      - Added support for custom serializers
      - Renamed SimpleCollection to EssentialCollection
* 0.4 - 12.30.2016 - Huge performance improvements from removing SimpleDocument dict wrapper
* 0.3 - 12.28.2016 - Added hashed indexes and documentation updates
* 0.2 - 12.18.2016 - Complete rewrite of query system to now precompile the query document.




