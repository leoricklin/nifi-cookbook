# Recipe 01: Extract json attribute
## Use case: 
read flow file of json format and extract attribute
## Approach:
refer [Need help on retrieving JSON attributes from a flow file in Apache NiFi](https://codedump.io/share/RaaSdBAf00tQ/1/need-help-on-retrieving-json-attributes-from-a-flow-file-in-apache-nifi)
## Examples:

* the output of url
```
$ curl --compressed -H "Accept: application/json" -X GET "http://localhost:8088/ws/v1/cluster/apps/application_1508258610180_0005"

{"app":{"id":"application_1508258610180_0005","user":"nifi","name":"HIVE-94ec3e1b-556f-4d29-b109-ab5fdce198d8","queue":"default","state":"FINISHED","finalStatus":"SUCCEEDED","progress":100.0,"trackingUI":"History","trackingUrl":"http://sandbox.kylo.io:8088/proxy/application_1508258610180_0002/","diagnostics":"null","clusterId":1509512076762,"applicationType":"TEZ","applicationTags":"","priority":0,"startedTime":1508280606527,"finishedTime":1508281043707,"elapsedTime":437180,"amContainerLogs":"http://sandbox.kylo.io:8042/node/containerlogs/container_e02_1508258610180_0002_01_000001/nifi","amHostHttpAddress":"sandbox.kylo.io:8042","allocatedMB":-1,"allocatedVCores":-1,"runningContainers":-1,"memorySeconds":868106,"vcoreSeconds":627,"queueUsagePercentage":0.0,"clusterUsagePercentage":0.0,"preemptedResourceMB":0,"preemptedResourceVCores":0,"numNonAMContainerPreempted":0,"numAMContainerPreempted":0,"logAggregationStatus":"NOT_START","unmanagedApplication":false,"amNodeLabelExpression":""}}
```

* GetHTTP

key | value
-|-
URL | http://localhost:8088/ws/v1/cluster/apps/application_1508258610180_0005
Filename | ${now():toNumber()}
Accept Content-Type | application/json

* EvaluateJsonPath

key | value
-|-
Destination | flowfile-content
Return Type | json
queuename | $.app.id

* PutFile

key | value
-|-
Directory | /home/nifi/output.log

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


# Recipe 02: Extract json array and route by index
## Use case: 
find the first element of a json array
## Approach:
refer [Converting a Large JSON File into CSV](https://community.hortonworks.com/articles/64069/converting-a-large-json-file-into-csv.html)
## Examples:

* the output of url
```
$ curl --compressed -H "Accept: application/json" -X GET "http://localhost:8088/ws/v1/cluster/apps/"

{
  "apps" : {
    "app" : [ {
      "id" : "application_1508258610180_0002",
      "user" : "nifi",
    }, {
      "id" : "application_1508454208332_0001",
      "user" : "hive",
    }, {
      "id" : "application_1508258610180_0003",
      "user" : "hive",
    }, {
      "id" : "application_1504645765786_0001",
      "user" : "nifi",
    }, {
      "id" : "application_1508258610180_0005",
      "user" : "nifi",
    }, {
      "id" : "application_1504645765786_0002",
      "user" : "nifi",
    }, {
      "id" : "application_1508258610180_0004",
      "user" : "nifi",
    }, {
      "id" : "application_1508258610180_0001",
      "user" : "nifi",
    } ]
  }
}
```

* GetHTTP

key | value
-|-
URL | http://localhost:8088/ws/v1/cluster/apps/
Filename | ${now():toNumber()}
Accept Content-Type | application/json

* SplitJson

key | value
-|-
Type | SplitJson 1.3.0
Automatically terminate relationships | failure , original
JsonPath Expression | $.apps.app
Null Value Representation | empty string

* Connection

key | value
-|-
From processor | SplitJson
To processor | UpdateAttribute
For relationships | split

* UpdateAttribute

key | value
-|-
Type | UpdateAttribute 1.3.0
filename | ${now():toNumber()}-${fragment.index}

* RouteOnAttribute

key | value
-|-
Type | RouteOnAttribute 1.3.0
Routing Strategy | Route to Property name
record-first | ${fragment.index:equals(0)}

* Connection

key | value
-|-
From processor | RouteOnAttribute
To processor | PutFile.01
Relationships | record-first

* PutFile.01

key | value
-|-
Directory | /home/nifi/output.log

* Connection

key | value
-|-
From processor | RouteOnAttribute
To processor | PutFile.02
Relationships | unmatched


* PutFile.02

key | value
-|-
Directory | /home/nifi/output.err


* execute nifi flow

* check the output
```
$ cat output.log/1510296498380-0
{"id":"application_1508258610180_0002","user":"nifi"}

$ ll output.err/
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498380-1
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498380-2
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498380-3
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498381-4
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498381-5
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498381-6
-rw-r--r-- 1 nifi nifi 991 Nov 10 06:48 1510296498381-7

$ cat output.err/1510296498380-1
{"id":"application_1508454208332_0001","user":"hive"}

$ cat output.err/1510296498380-2
{"id":"application_1508258610180_0003","user":"hive"}

$ cat output.err/1510296498381-7
{"id":"application_1508258610180_0001","user":"nifi"}

```
