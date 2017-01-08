
Serializers
============

EssentialDB does not currently support any partitioning or sharding schemes, so data is written and loaded to disk at
once. This is okay, since EssentialDB is designed to be used mostly in-memory, but it means that disk writes are
expensive. We did some fairly extensive `benchmarking of Python 3 serializers <http://www.wrong.dog/python_serializers/>`_
and found that Pickle is the fastest and most versatile serialization techniques and is the default mechanism in EssentialDB
for (de)serializing documents on disk.

Recognizing there are plenty of times when another format might be desired, version 0.5 adds support for Python's built-in
JSON (de)serializer by adding the 'serializer' flag. You can invoke like this::

    import essentialdb
    db =  essentialdb.EssentialDB(filepath=self.path, serializer=essentialdb.JSONSerializer())

What if you want to use something else though? Like ujson or msg-pack? Simply define your own storage class that implement
the load and dump methods::

    import msgpack
    import essentialDB

    class MsgPackSerializer:
        """
        Implements a basic (de)serializer based on MessagePack.
        """

        @staticmethod
        def load(file_path):
            with open(file_path, 'rb') as fp:
                data = msgpack.unpack(fp, encoding='utf-8')
            return data

        @staticmethod
        def dump(data, file_path):
            with open(file_path, 'wb') as fp:
                msgpack.pack(output, fp, use_bin_type=True)

    db =  essentialdb.EssentialDB(filepath=self.path, serializer=essentialdb.MsgPackSerializer())


Beaware though, serializers not based on pickle will likely perform slower in most use cases. Assitionally, they will not
natively support many Python types (like datetime). You can add those to most serializers with custom hooks. EssentialDB
does not include native support for non-builtin (de)serializers to avoid external dependencies.
