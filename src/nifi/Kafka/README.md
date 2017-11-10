# Recipe 01: Consume message from Kafka brokers and publish to brokers
## Use case: 
establish the performance baseline
## Approach:
refer [20160919 Integrating Apache NiFi and Apache Kafka](https://community.hortonworks.com/articles/57262/integrating-apache-nifi-and-apache-kafka.html)
## Examples:

* measure the throughput of broker by kafka utility
```
$ export base_dir=/usr/hdp/current/kafka-broker
$ BROKERS="p130:9092,p131:9092,p132:9092";\
CONSUME_GRP=`date +%Y%m%d%H%M`;\
TOPICS="topics";\
THREADS=12;\
LOG="/home/nifi/${TOPICS}-${CONSUME_GRP}.log";\
$base_dir/bin/kafka-consumer-perf-test.sh --broker-list ${BROKERS} --group ${CONSUME_GRP} --message-size 1000 --messages 50000000 --threads ${THREAD} --topic ${TOPIC} > ${LOG} 2>&1
```

* ConsumeKafka

key | value
-|-
Type | ConsumeKafka_0_10 1.2.0.3.0.0.0-453
Penalty duration | 30 sec
Yield duration | 0 sec
Scheduling strategy | Timer driven
Concurrent tasks | 2
Run schedule | 0 sec
Execution | All nodes
Run duration | 00:00:00.000
Kafka Brokers | p130:9092,p131:9092,p132:9092
Topic Name(s) = topics
Group ID | 201711101200
Message Demarcator | 1qaz2wsx
Max Poll Records | 20000
Max Uncommitted Time | 3 secs
max.partition.fetch.bytes | 10485760
receive.buffer.bytes | 1048576

* PublishKafka

key | value
-|-
Type | PublishKafka_0_10 1.2.0.3.0.0.0-453
Penalty duration | 30 sec
Yield duration | 1 sec
Scheduling strategy | Timer driven
Concurrent tasks | 5
Run schedule | 0 sec
Execution | All nodes 
Run duration | 00:00:00.000
Kafka Brokers | p130:9092,p131:9092,p132:9092
Topic Name(s) = newtopics
Delivery Guarantee | Best Effort
Message Demarcator | 1qaz2wsx
Max Request Size | 1 MB
Acknowledgment Wait Time | 5 secs
Max Metadata Wait Time | 5 sec
Partitioner class | DefaultPartitioner
Compression Type | none


* execute nifi flow

* consume the output by kafka utility
```
$ export base_dir=/usr/hdp/current/kafka-broker
$ BROKERS="p130:9092,p131:9092,p132:9092";\
CONID=`date +%Y%m%d%H%M`;\
TOPIC="topics";\
LOG="/home/nifi/${TOPICS}-${CONID}.log";\
$base_dir/bin/kafka-console-consumer.sh --consumer-property group.id="${CONID}" --bootstrap-server ${BROKERS} --topic ${TOPIC} > ${LOG} &
```
