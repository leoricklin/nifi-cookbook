# Recipe 01: Extract json attribute
## Use case: 
read flow file of json format and extract attribute
## Approach:
refer [Need help on retrieving JSON attributes from a flow file in Apache NiFi](https://codedump.io/share/RaaSdBAf00tQ/1/need-help-on-retrieving-json-attributes-from-a-flow-file-in-apache-nifi)
## Examples:

* the output of url
```
$ curl --compressed -H "Accept: application/json" -X GET "http://localhost:8088/ws/v1/cluster/apps/application_1508258610180_0002"

{"app":{"id":"application_1508258610180_0002","user":"nifi","name":"HIVE-94ec3e1b-556f-4d29-b109-ab5fdce198d8","queue":"default","state":"FINISHED","finalStatus":"SUCCEEDED","progress":100.0,"trackingUI":"History","trackingUrl":"http://sandbox.kylo.io:8088/proxy/application_1508258610180_0002/","diagnostics":"null","clusterId":1509512076762,"applicationType":"TEZ","applicationTags":"","priority":0,"startedTime":1508280606527,"finishedTime":1508281043707,"elapsedTime":437180,"amContainerLogs":"http://sandbox.kylo.io:8042/node/containerlogs/container_e02_1508258610180_0002_01_000001/nifi","amHostHttpAddress":"sandbox.kylo.io:8042","allocatedMB":-1,"allocatedVCores":-1,"runningContainers":-1,"memorySeconds":868106,"vcoreSeconds":627,"queueUsagePercentage":0.0,"clusterUsagePercentage":0.0,"preemptedResourceMB":0,"preemptedResourceVCores":0,"numNonAMContainerPreempted":0,"numAMContainerPreempted":0,"logAggregationStatus":"NOT_START","unmanagedApplication":false,"amNodeLabelExpression":""}}
```

* GetHTTP
```
URL = http://localhost:8088/ws/v1/cluster/apps/application_1508258610180_0005
Filename = ${now():toNumber()}
Accept Content-Type = application/json
```

* EvaluateJsonPath
```
Destination = flowfile-content
Return Type = json
queuename = $.app.id
```

* PutFile
```
Directory = /home/nifi/output.log
```

* clean up output directory
```
$ rm -f /home/nifi/output.log/*
```

* execute nifi flow

* check the output
```
$ cat output.log/1510225424124
application_1508258610180_0005
```

