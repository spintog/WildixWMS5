Wildix Integration - Python
=======================
This python module is used to send HTTP requests to the new WMS5 API and integrate with other systems.

## Example 

### Create instance
```python
config = {
    "pbx_secret_key": "Secret",
    "app_id": "app-id",
    "app_name": "app-name",
    "pbx_host": "your_pbx.wildixin.com"
}

client = Client(config)
```

### Send HTTP request with GET method
This example gets call history from PBX for all users.

API Documentation in https://www.wildix.com/wp-content/wms-api/
```python

//example params
options = {
    "url": "/api/v1/PBX/CallHistory/",
    "fields": "id,start,end,src,dst",
    "filter": {
        "start": {
            "from": "02/11/2020 00:01",
            "to": "01/11/2020 23:59",
        },
        "count": "3",
        "start": "3",
    }
}

query_result = pbx_connection.query_get("/api/v1/PBX/Colleagues/", options)
```

### Send HTTP request with POST method
This example create a new Colleague.

API Documentation in https://www.wildix.com/wp-content/wms-api/
```python

//example params
options = {
    "number": 1237,
    "name": "TestUser",
}

query_result = pbx_connection.query_post("/api/v1/PBX/Colleagues/", options)
```
