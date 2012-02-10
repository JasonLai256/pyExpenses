#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
    pyExpenses.utils
    ~~~~~~~~~~~~~~~~

    Implements various utilities functions or class.

    :copyright: (c) 2012 by Jason Lai.
    :license: BSD, see LICENSE for more details.
"""

import csv
import cStringIO
import codecs
from datetime import date

import ErrorHandle as EH
from Record import BaseRecord


def datecheck(date):
    """检查date的格式是否符合ISO格式 'yyyy-mm-dd' """
    if date[4] == '-' and date[7] == '-':
        return True
    return False

def to_date(da):
    """假设da的格式为'yyyy-mm-dd'."""
    if isinstance(da, date):
        return da
    elif isinstance(da, (str, unicode)):
        if datecheck(da):
            y = int(da[:4])
            m = int(da[5:7])
            d = int(da[8:])
            return date(y, m, d)
    else:
        EH.valueError('date ({0}) format error.'.format(str(da)))

def buf2record(buf):
    rdate = to_date(buf[0])
    rtype = buf[2], buf[3]
    rec = BaseRecord(buf[1], rtype, buf[4], buf[5], buf[6], buf[7])
    return rdate, rec

def record2buf(rdate, rec):
    return [
        rdate.isoformat(),
        rec.amount,
        rec.type[0],
        rec.type[1],
        rec.payment,
        rec.currency,
        rec.tag,
        rec.comment
    ]


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
