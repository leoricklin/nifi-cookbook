# Recipe 01: Modify flow file content
## Use case: 
read and modify flow file content
## Approach:
refer [ExecuteScript Cookbook (part 1)](https://community.hortonworks.com/articles/75032/executescript-cookbook-part-1.html)
## Examples:

* ExecuteProcess

key | value
-|-
Command | /home/nifi/run1.sh
MSG | this is message

* ExecuteScript

key | value
-|-
Script Engine | ECMAScript
Script Body |
var InputStreamCallback =  Java.type("org.apache.nifi.processor.io.InputStreamCallback");
var OutputStreamCallback =  Java.type("org.apache.nifi.processor.io.OutputStreamCallback");
var IOUtils = Java.type("org.apache.commons.io.IOUtils");
var StandardCharsets = Java.type("java.nio.charset.StandardCharsets");
 
var flowFile = session.get();
if(flowFile != null) {
  try {
  // Create a new InputStreamCallback, passing in a function to define the interface method
  var text = "";
  session.read(flowFile,
    new InputStreamCallback(function(inputStream) {
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8);
        // Do something with text here
    }));
  text = text + "qazwsx";
  flowFile = session.write(flowFile,
    new OutputStreamCallback(function(outputStream) {
        outputStream.write(text.getBytes(StandardCharsets.UTF_8))
    }));
  session.transfer(flowFile, REL_SUCCESS)
  } catch(e) {
    log.error('Something went wrong', e)
    session.transfer(flowFile, REL_FAILURE)
  }
}


* PutFile

key | value
-|-
Directory | /home/nifi/output.log

* chmod & clean up output directory
```
$ chmod 755 /home/nifi/run1.sh
$ rm -f /home/nifi/output.log/*
```

* execute nifi flow

* check the output
```
$ cat /home/nifi/output.log/42190644392215
hello
world
i'm john
MSG=this is message
qazwsx
```

# Recipe 02: Parsing flow file content
## Use case: 
read the content of input flow file and write new content to output flow file
## Approach:
refer [ExecuteScript Cookbook (part 2)](https://community.hortonworks.com/articles/75545/executescript-cookbook-part-2.html)
## Examples:

* ExecuteProcess

key | value
-|-
Command = /home/nifi/02-1.sh
MSG = this is message

* ExecuteScript

key | value
-|-
Script Engine = python
Script File = /home/nifi/02-1.py

* PutFile

key | value
-|-
Directory = /home/nifi/output.log

* chmod & clean up output directory
```
$ chmod 755 /home/nifi/02-1.sh
$ rm -f /home/nifi/output.log/*
```

* execute nifi flow

* check the output
```
$ cat /home/nifi/output.log/65288338611032
insert into tab (key, value) values ('successRate (1000/1000)','100.00%');
insert into tab (key, value) values ('avgDuration','0:04:43');
insert into tab (key, value) values ('overwriteRate','89.70%');
```

# Recipe 03: Using Dynamic Properties
## Use case: 
read the content and variables of input flow file and write new content to output flow file
## Approach:
refer [ExecuteScript Cookbook (part 3)](https://community.hortonworks.com/articles/77739/executescript-cookbook-part-3.html)
## Examples:

* ExecuteProcess

key | value
-|-
Command | /home/nifi/02-1.sh
MSG | this is message

* ExecuteScript

key | value
-|-
Script Engine | python
Script File | /home/nifi/03-1.py
actionname | record-sample
feedname | ran.bdokafka-bdoredis

* PutFile

key | value
-|-
Directory | /home/nifi/output.log

* chmod & clean up output directory
```
$ chmod 755 /home/nifi/02-1.sh
$ rm -f /home/nifi/output.log/*
```

* execute nifi flow

* check the output
```
$ cat output.log/102548350037196
insert into tab (who, what, when, where, key, value) values ('ran.bdokafka-bdoredis','record-sample','1510200702','sandbox.kylo.io','successRate (1000/1000)','100.00%');
insert into tab (who, what, when, where, key, value) values ('ran.bdokafka-bdoredis','record-sample','1510200702','sandbox.kylo.io','avgDuration','0:04:43');
insert into tab (who, what, when, where, key, value) values ('ran.bdokafka-bdoredis','record-sample','1510200702','sandbox.kylo.io','overwriteRate','89.70%');
```

# Recipe 04: Read the value of Nifi Expression
## Use case: 
read the value of Nifi expression
## Approach:
* set the dynamic properties of ExecuteScript with Nifi Expression, e.g: ${fileSize:toNumber():toString()} 
* read the dynamic properties in script block
## Examples:
