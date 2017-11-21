# Tracking

[![Travis](https://img.shields.io/travis/datahq/events/master.svg)](https://travis-ci.org/datahq/events)
[![Coveralls](http://img.shields.io/coveralls/datahq/events.svg?branch=master)](https://coveralls.io/r/datahq/events?branch=master)

### Manage event broadcasting

```python
send_event(entity,       # Source of the event
           action,       # What happened
           status,       # Success indication: "OK"/Error message
           findability,  # one of "published/private/internal":
                         #  - public: visible to all
                         #  - private: visible just to the user
                         #  - internal: visible only to admin (i.e. never returns via api)
           userid,       # Actor
           dataset_id,   # Dataset in question 
           owner,        # Owner of the dataset
           ownerid,      # Owner of the dataset
           flow_id,      # Related flow id 
           pipeline_id,  # Related pipeline id
           payload       # Other payload
)
```

## Contributing

Please read the contribution guideline:

[How to Contribute](CONTRIBUTING.md)

Thanks!
