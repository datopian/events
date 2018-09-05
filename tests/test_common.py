# -*- coding: utf-8 -*-
import pytest
import time

from events import events
import elasticsearch


@pytest.fixture()
def es():
    es = elasticsearch.Elasticsearch()
    es.indices.delete(index=events.EVENTS_INDEX_NAME, ignore=[400, 404])
    es.indices.flush()
    return es


def test_send(es: elasticsearch.Elasticsearch):
    events.send_event('entity',
                      'action',
                      'status',
                      'findability',
                      'userid',
                      'dataset_id',
                      'owner',
                      'ownerid',
                      'flow_id',
                      'pipeline_id',
                      'payload')
    events.tpe.shutdown(True)
    time.sleep(2)
    sources = es.search(index=events.EVENTS_INDEX_NAME)
    hits = sources['hits']['hits']
    expected = {
        'event_entity': 'entity',
        'event_action': 'action',
        'status': 'status',
        'findability': 'findability',
        'userid': 'userid',
        'dataset': 'dataset_id',
        'owner': 'owner',
        'ownerid': 'ownerid',
        'flow': 'flow_id',
        'pipeline': 'pipeline_id',
        'payload': 'payload',
    }
    assert len(hits) == 1
    for k, v in expected.items():
        assert hits[0]['_source'][k] == v
