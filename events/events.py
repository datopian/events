import datetime
import logging
import os
from concurrent.futures import ThreadPoolExecutor

import elasticsearch

tpe = ThreadPoolExecutor(max_workers=1)

ELASTICSEARCH_HOST = os.environ.get('EVENTS_ELASTICSEARCH_HOST', 'localhost:9200')
EVENTS_INDEX_NAME = os.environ.get('EVENTS_INDEX_NAME', 'events')


def _send(es: elasticsearch.Elasticsearch,
          entity,       # Source of the event
          action,       # What happened
          status,       # Success indication
          findability,  # one of "published/private/internal":
          userid,       # Actor
          dataset_id,   # Dataset in question
          owner,      # Owner of the dataset
          ownerid,      # Owner of the dataset
          flow_id,      # Related flow id
          pipeline_id,  # Related pipeline id
          payload       # Other payload
          ):
    now = datetime.datetime.now()
    body = {
        "event_entity": entity,
        "event_action": action,
        "status": status,
        "findability": findability,
        "userid": userid,
        "dataset": dataset_id,
        "owner": owner,
        "ownerid": ownerid,
        "flow": flow_id,
        "pipeline": pipeline_id,
        "payload": payload,
        "timestamp": now.isoformat()
    }
    success = es.index(EVENTS_INDEX_NAME, 'event', body)
    if not success:
        logging.warning('Failed to push event to %s, %r', EVENTS_INDEX_NAME, body)


class EventSender():
    def __init__(self):
        self.es = elasticsearch.Elasticsearch(hosts=[ELASTICSEARCH_HOST])

    def __call__(self, *args, **kwargs):
        tpe.submit(_send, self.es, *args)


send_event = EventSender()
