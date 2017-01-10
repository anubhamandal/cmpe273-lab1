## Twisted for writing an Async Http Client

### Requirement

* Run 2-3 replicas of a server on different ports in local machine (can be used with external links as well).
* Buila a client to send async calls to all the replicas using Twisted.
* Find the closet server based on the latency from the set of replicas.