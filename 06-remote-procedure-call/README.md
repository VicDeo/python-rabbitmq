# Remote procedure call

* Producer acts as a client and consumer acts as a server
* Producer requests the processing from the subscriber and waits for the response
* Producer provides reply queue as a parameter
* Producer provides a correlation id (job id)
* The response is discarded if the correlation id of response doesn't match request correlation id
* Typically the subscriber sends acknowledgement to the queue only after it sent the response to the producer via tha reply queue
* Producer sends acknowledgement right after reading the response
* Server queue may not be exclusive
* Reply queue should be exclusive and should have a specific processing method

`client.py` sends a request to the RPC server and get a response back
`server.py` gets a parameter, makes calculations and sends the result back to the client

