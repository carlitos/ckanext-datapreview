"""Data Proxy - CSV transformation adapter"""
import urllib2
import xml.dom.minidom
from xml.parsers.expat import ExpatError
from ckanext.datapreview.transform.base import Transformer

import brewery.ds as ds

try:
    import json
except ImportError:
    import simplejson as json

class XMLTransformer(Transformer):
    """
    Transforms XML based formats (atom, xml, rss, rdf etc) and pretty prints
    the output so that it is delivered in a readable format.
    """

    def __init__(self, resource, url, query):
        super(XMLTransformer, self).__init__(resource, url, query)
        self.requires_size_limit = True

    def transform(self):
        handle = self.open_data(self.url)
        if not handle:
            return dict(title="Remote resource missing",
                message="Unable to load the remote resource")

        data = handle.read()
        print data[0:50]
        try:
            dom = xml.dom.minidom.parseString(data)
            pretty = dom.toprettyxml(indent='   ')
        except ExpatError as ee:
            self.close_stream(handle)

            return dict(title="Invalid content",
                    message="This content does not appear to be valid XML")
        except Exception as e:
            print self.url
            raise e
        result = {
                    "fields": ["data"],
                    "data": [["%s" % (pretty)]]
                  }

        self.close_stream(handle)

        return result
