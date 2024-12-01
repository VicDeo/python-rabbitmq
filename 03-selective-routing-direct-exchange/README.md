# Selective Routing / Direct Exchange

* Many to Many
* Producers are not aware of message queues or consumers 
* Consumer creates a queue and binds it to the routing key of interest
* It is possible to have more than one binding per consumer
* It is possible for the different consumers to have duplicated routing keys
* Messages that match no rules are discarded
* Routing is done by the exchange basing on the binding rules 

`producer.py` produces multiple emergency messages sent to different routes
`consumer-police.py` consumes messages with the routing key of "Baboon" or "Donkey"
`consumer-gang.py` consumes messages with the routing key of "Badger", "Donkey" or "Racoon"
