# Pattern Based Routing / Topic Exchange

* Many to Many
* Producers are not aware of message queues or consumers 
* Consumer creates a queue and binds it to the exchange
* It is possible to have more than one binding per consumer
* Messages are merged for the same consumer so even if many bindings of the same consumer match the same message, it will be received by the consumer only once
* It is possible for the different consumers to have the same binding rules
* Multiple consumers can bind to the same queue (if the queue is not exclusive). In this case they got messages in a Round Robin fashion - this is a queue feature 
* Messages that match no rules are discarded
* Routing is done by the exchange basing on the binding rules 
* Routing keys contain stars(*) and hashes(#) with a special meaning. Star means '1 word' while has means '0 or more words'  

`producer.py` produces multiple messages sent to different routes depending on the message priority and category
`consumer-1.py` consumes messages with the priority High
`consumer-2.py` consumes messages with the category Alert
`consumer-3.py` consumes messages with the priority High and the category Complaint
`consumer-4.py` consumes all messages

