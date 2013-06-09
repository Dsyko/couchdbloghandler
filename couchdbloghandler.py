__author__ = 'dsyko'
"""
couchdbloghandler.py

A python logging handler using CouchDB for log storage

Requires Python 2.7+, CouchDB 0.9+, see https://pypi.python.org/pypi/CouchDB, or easy_install CouchDB
"""

import logging
import couchdb
import time
from uuid import uuid4
import json


def pretty(text):
        return json.dumps(text, indent = 4, sort_keys = True)

class CouchDBLogHandler(logging.Handler):

    def __init__(self, dbname, server="http://localhost:5984/", doctype="log"):
        """
        @param dbname: Name of the CouchDB database
        @param server: URL pointing to the CouchDB instance we want to log to
        @param doctype: value to set the doc_type to in the json object posted to the couchdb
        """
        logging.Handler.__init__(self, level=logging.INFO)

        couchServer = couchdb.Server(server)
        if dbname not in couchServer:
            self.loggingDatabase = couchServer.create(dbname)
        else:
            self.loggingDatabase = couchServer[dbname]

        self.doctype = doctype

        # Testing DB, write a record and then delete it. This will throw errors if the db isn't working properly
        docID, docREV = self.loggingDatabase.save({"doc_type": self.doctype, "message": "Testing"})
        self.loggingDatabase.delete({'_id': docID, '_rev': docREV})

    def emit(self, record):
        try:
            logtime = record.asctime
        except AttributeError:
            logtime = time.asctime()

        #Record data to push to couchDB
        data = {
            "_id": uuid4().hex,
            "doc_type": self.doctype,
            "logger_name": record.name,
            "module_name": record.module,
            "level": record.levelname,
            "date": logtime,
            "time": int(time.time()*100000),  #Time in microseconds since epoch
            "message": record.msg
        }

        #Push it to couchDB
        self.loggingDatabase.save(data)

#Following code will only be executed if this module is run independently, not when imported. Use it to test the module.
if __name__ == "__main__":

    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    couchHandler = CouchDBLogHandler("testing-couchdb-logger", server="http://localhost:5984/")
    logger.addHandler(couchHandler)

    msg = "test logging message"
    numRecords = 10

    print "running test"

    start = time.time()
    elapsed = 0.0
    for i in range(0,numRecords):
        emitstart = time.time()
        logger.info(msg)
        emitend = time.time()
        elapsed += (emitend - emitstart)

    end = time.time()



    total = end - start
    print "couchdb handler test took %s seconds, averaging %d ms per log entry" % (str(elapsed), (elapsed / numRecords) * 1000)
    print "check that testing-couchdb-logger database exists on your couch, and delete it if you don't want it there."

