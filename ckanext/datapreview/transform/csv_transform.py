"""Data Proxy - CSV transformation adapter"""
import urllib2
import csv
from ckanext.datapreview.transform.base import Transformer
import brewery.ds as ds

try:
    import json
except ImportError:
    import simplejson as json

class CSVTransformer(Transformer):
    def __init__(self, resource, url, query):
        super(CSVTransformer, self).__init__(resource, url, query)
        self.requires_size_limit = False

        if 'encoding' in self.query:
            self.encoding = self.query["encoding"]
        else:
            self.encoding = 'utf-8'

        if 'dialect' in self.query:
            self.dialect = self.query["dialect"]
        else:
            self.dialect = None

    def transform(self):
        handle = self.open_data(self.url)

        if not self.dialect:
            if self.url.endswith('.tsv'):
                self.dialect = 'excel-tab'
            else:
                self.dialect = 'excel'

        src = ds.CSVDataSource(handle, encoding=self.encoding, dialect=self.dialect)
        src.initialize()

        result = self.read_source_rows(src)
        handle.close()

        return result

