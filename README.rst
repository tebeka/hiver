What?
=====
Packing hive thrift client in more Pythonic way.

Why?
====
Hive thrift libraries taken from CDH4 distribution and then mucked around to make
the imports work.

How?
====
In code
-------
::
    
    import hiver
    client = hiver.connect(host, port)
    client.execute('SHOW TABLES')
    rows = client.fetchAll()

Command line
------------
Poor mans hive client

::

    python -m hiver [script]

Who?
====
https://bitbucket.org/tebeka/hive
