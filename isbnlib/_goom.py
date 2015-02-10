# -*- coding: utf-8 -*-
"""Query the Google Books (JSON API v1) for metadata."""

import logging

from .dev import stdmeta
from .dev._exceptions import (DataWrongShapeError, NoDataForSelectorError,
                              RecordMappingError)
from .dev.bouth23 import u
from .dev.webquery import query as wquery


UA = 'isbntools (gzip)'
SERVICE_URL = 'https://www.googleapis.com/books/v1/volumes?q={words}'\
    '&fields=items/volumeInfo(title,authors,publisher,publishedDate,'\
    'language,industryIdentifiers)&maxResults=10'
LOGGER = logging.getLogger(__name__)


def _mapper(record):
    """Map canonical <- record."""
    # canonical:
    # -> ISBN-13, Title, Authors, Publisher, Year, Language
    try:
        # mapping: canonical <- records
        if 'industryIdentifiers' not in record:  # pragma: no cover
            return
        canonical = {}
        isbn = None
        for ident in record['industryIdentifiers']:
            if ident['type'] == 'ISBN_13':
                isbn = ident['identifier']
                break
        if not isbn:  # pragma: no cover
            return
        canonical['ISBN-13'] = isbn
        canonical['Title'] = record.get('title', u('')).replace(' :', ':')
        canonical['Authors'] = record.get('authors', [])
        canonical['Publisher'] = record.get('publisher', u(''))
        if 'publishedDate' in record \
           and len(record['publishedDate']) >= 4:
            canonical['Year'] = record['publishedDate'][0:4]
        else:         # pragma: no cover
            canonical['Year'] = u('')
        canonical['Language'] = record.get('language', u(''))
    except:           # pragma: no cover
        raise RecordMappingError(isbn)
    # call stdmeta for extra cleanning and validation
    return stdmeta(canonical)


def _records(words, data):
    """Classify (canonically) the parsed data."""
    try:
        # put the selected data in records
        records = [d['volumeInfo'] for d in data['items']]
    except:           # pragma: no cover
        try:
            extra = data['stat']
            LOGGER.debug('DataWrongShapeError for %s with data %s',
                         words, extra)
        except:
            raise DataWrongShapeError(words)
        raise NoDataForSelectorError(words)

    # map canonical <- records
    return [_mapper(r) for r in records if _mapper(r)]


def query(words):
    """Query the Google Books (JSON API v1) for metadata."""
    data = wquery(SERVICE_URL.format(words=words.replace(' ', '+')), UA)
    return _records(words, data)
