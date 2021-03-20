from elasticsearch import Elasticsearch
import lorem
import names


def create_sample_index(es: Elasticsearch, index_name: str, params=None, headers=None):
    return es.indices.create(
        index=index_name,
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "category": {
                        "type": "keyword"
                    },
                    "content": {
                        "type": "text"
                    },
                    "join_field": {
                        "type": "join",
                        "relations": {
                            "item": "fragment"
                        }
                    }
                }
            }
        },
        params=params,
        headers=headers
    )


def load_sample_data(es: Elasticsearch, index_name: str, num_docs=10, params=None, headers=None):
    for i in range(num_docs):
        body = {
            "name": names.get_full_name(),
            "category": f"person_type_{i % 2}",
            "join_field": "item",
        }
        print(f"Creating sample data {body}.")
        res = es.index(index=index_name,
                       doc_type="_doc",
                       routing=1,
                       body=body,
                       params=params,
                       headers=headers)
        doc_id = res["_id"]
        print(f"Created with id {doc_id}.")
        fragment_body = {
            "content": lorem.paragraph(),
            "join_field": {
                "name": "fragment",
                "parent": doc_id,
            },
        }
        print(f"Creating sample fragment data {fragment_body}.")
        res = es.index(index=index_name,
                       doc_type="_doc",
                       routing=1,
                       body=fragment_body,
                       params=params,
                       headers=headers)
        doc_id = res["_id"]
        print(f"Created with id {doc_id}.")


def load_sample_config(es: Elasticsearch, index_name: str, params=None, headers=None):
    config = {
        "title": "Sample Search",
        "config": {
            "fields": ["search", "mediaType", "page", "rows", "date"],
            "filters": [
                {
                    "type": "text",
                    "field": "search"
                }
            ]
        }
    }
    es.index(index=index_name,
             doc_type="_doc",
             id="sample",
             routing=1,
             body=config,
             params=params,
             headers=headers)
