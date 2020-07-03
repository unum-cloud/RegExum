import copy

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from PyWrappedDocs.BaseAPI import BaseAPI
from PyWrappedHelpers.Algorithms import *
from PyWrappedHelpers.TextFile import TextFile
from PyWrappedHelpers.Config import allow_big_csv_fields


class ElasticSearch(BaseAPI):
    """
        ElasticSearch is built on top of Lucene, but Lucene is  
        hard to install on its own. So we run the full version.

        https://www.elastic.co
        https://elasticsearch-py.readthedocs.io/en/master/
        https://www.elastic.co/guide/en/elasticsearch/reference/current/brew.html
    """
    __is_concurrent__ = False
    __max_batch_size__ = 100000
    __in_memory__ = False

    def __init__(self, url='http://localhost:9200/text', **kwargs):
        BaseAPI.__init__(self, **kwargs)
        url, db_name = extract_database_name(url, default='text')
        self.elastic = Elasticsearch([url])
        self.db_name = db_name
        self.create_index()

    def create_index(self):
        if self.index_exists():
            return
        properties = dict()
        for field in self.indexed_fields:
            properties[field] = {'type': 'text'}
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-create-index.html
        # https://sarahleejane.github.io/learning/python/2015/10/14/creating-an-elastic-search-index-with-python.html
        self.elastic.indices.create(self.db_name, body={
            'settings': {
                'number_of_shards': 1,
            },
            'mappings': {
                'properties': properties,
            }
        })

    def index_exists(self):
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-exists.html
        return self.elastic.indices.exists(self.db_name)

    def commit_all(self):
        return self.elastic.indices.refresh(self.db_name)

    def remove_all(self):
        # https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-exists.html
        if self.index_exists():
            self.elastic.indices.delete(self.db_name)
        self.create_index()

    def count_docs(self) -> int:
        if not self.index_exists():
            return 0
        return self.elastic.count(index=self.db_name).pop('count', 0)

    def validate_doc(self, doc: object) -> dict:
        if isinstance(doc, (str, int)):
            return {'_id': doc}
        if isinstance(doc, TextFile):
            return doc.to_dict()
        if isinstance(doc, dict):
            return copy.deepcopy(doc)
        return copy.deepcopy(doc.__dict__)

    def upsert_doc(self, doc, sync=True) -> bool:
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html
        doc = self.validate_doc(doc)
        doc_id = doc.pop('_id', None)
        if doc_id is None:
            return False
        result = self.elastic.index(index=self.db_name, id=doc_id, body=doc)
        result = result.pop('result', None)
        if (result == 'created') or (result == 'updated'):
            if sync:
                self.commit_all()
            return True
        return False

    def remove_doc(self, doc, sync=True) -> bool:
        doc = self.validate_doc(doc)
        doc_id = doc.pop('_id', None)
        if doc_id is None:
            return False
        result = self.elastic.delete(index=self.db_name, id=doc_id)
        result = result.pop('result', None)
        if (result == 'deleted'):
            if sync:
                self.commit_all()
            return True
        return False

    def upsert_docs(self, docs) -> int:
        docs = map(self.validate_doc, docs)
        statuses = [self.upsert_doc(doc, sync=False) for doc in docs]
        self.commit_all()
        return sum(statuses)

    def remove_docs(self, docs) -> int:
        docs = map(self.validate_doc, docs)
        statuses = [self.remove_doc(doc, sync=False) for doc in docs]
        self.commit_all()
        return sum(statuses)

    def hit_to_dict(self, hit: dict) -> dict:
        content = hit['_source']
        content['_id'] = hit['_id']
        if '_score' in hit:
            content['_score'] = hit['_score']
        return content

    def find_with_id(self, identifier: str):
        """ 
            Returns the document together with it's system ID, that may be different from original once.
            It's done to reduce the DB size and accelerate the search.
            https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html
        """
        doc = self.elastic.get(index=self.db_name, id=identifier)
        if doc is None:
            return None
        if not doc.get('found', False):
            return None
        return self.hit_to_dict(doc)

    def find_with_substring(
        self,
        query: str,
        field: str = 'plain',
        max_matches: int = None,
    ):
        """
            Returns only document IDs without the content or match range.
            It's done to minimize the communication time and reduce the load on TCP/IP stack.
            We are benchmarking the DBs and not networking implementatinos, after all.
            https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-term-query.html
        """
        query_dict = {
            'query': {
                'term': {
                    field: query,
                }
            },
            'stored_fields': [],
        }
        if max_matches is not None:
            query_dict['from'] = 0
            query_dict['size'] = max_matches
        docs = self.elastic.search(index=self.db_name, body=query_dict)
        hits_arr = docs.get('hits', {}).get('hits', [])
        return [h['_id'] for h in hits_arr]

    def find_with_regex(
        self,
        query: str,
        field: str = 'plain',
        max_matches: int = None,
    ):
        """
            Returns only document IDs without the content or match range.
            It's done to minimize the communication time and reduce the load on TCP/IP stack.
            We are benchmarking the DBs and not networking implementatinos, after all.
            https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-regexp-query.html
            https://lucene.apache.org/core/4_9_0/core/org/apache/lucene/util/automaton/RegExp.html
        """
        query_dict = {
            'query': {
                'regexp': {
                    field: {
                        'value': query,
                        'flags': 'INTERVAL',
                    }
                }
            },
            'stored_fields': [],
        }
        if max_matches is not None:
            query_dict['from'] = 0
            query_dict['size'] = max_matches
        docs = self.elastic.search(index=self.db_name, body=query_dict)
        hits_arr = docs.get('hits', {}).get('hits', [])
        return [h['_id'] for h in hits_arr]

    def import_docs_from_csv(self, filepath: str) -> int:
        allow_big_csv_fields()
        # https://elasticsearch-py.readthedocs.io/en/master/helpers.html

        def produce_validated():
            for doc in yield_texts_from_sectioned_csv(filepath):
                yield self.validate_doc(doc)

        cnt_success = 0
        for ok, action in streaming_bulk(
            client=self.elastic,
            index=self.db_name,
            actions=produce_validated(),
        ):
            cnt_success += ok
        return cnt_success


if __name__ == '__main__':
    sample_file = 'Datasets/text-test/nanoformulations.txt'
    db = ElasticSearch(url='http://localhost:9200/text-test')
    db.remove_all()
    assert db.count_docs() == 0
    assert db.upsert_doc(TextFile(sample_file).to_dict())
    assert db.count_docs() == 1
    assert db.find_with_substring('nanoparticles')
    assert db.find_with_regex('nanoparticles')
    assert db.remove_doc(TextFile(sample_file).to_dict())
    assert db.count_docs() == 0
