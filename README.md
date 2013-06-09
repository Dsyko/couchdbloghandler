couchDB Loghandler
=================

Python log handler for logging to a couchDB

This handler is dependent on Python 2.7+ and the [CouchDB package](https://pypi.python.org/pypi/CouchDB)
You can use easy_install to get CouchDB package installed like so:

```
easy_install CouchDB
```

Once that dependency is squared away you're ready to use the handler:

```python

    import logging
    import couchdbloghandler

    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    couchHandler = CouchDBLogHandler("testing-couchdb-logger", server="http://localhost:5984/", doctype="log")
    logger.addHandler(couchHandler)

    #now we are ready to use our logger, message will be saved to the DB
    logger.info("Your logs here.")
```

The previous code will create the DB, "testing-couchdb-logger" if it doesn't already exist on the couchDB hosted at http://localhost:5984/
The saved document will have the following format:

```javascript
{
    "_id": DocumentUniqueID,
    "doc_type": "log"                   //Defaulst to "log". Changed by passing doctype="your doctype" to handler constructor
    "logger_name": "test"               //name given to logger with logging.getLogger()
    "module_name": "module name"        //name of module logger was called from
    "level": "INFO"                     //level logger was called with
    "date": "Sun Jun  9 03:11:33 2013"  //Human readable date and time
    "time": 137077269340502,            //Time in microseconds since epoch
    "message": "Your logs here."        //Log message...
}
```


