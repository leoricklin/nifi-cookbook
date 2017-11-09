# Recipe 01: Modify flow file content
## Use case: 
read and modify flow file content
## Approach:
refer [ExecuteScript Cookbook (part 1)](https://community.hortonworks.com/articles/75032/executescript-cookbook-part-1.html)
## Examples:
* change file mode & clean up output directory
```
$ chmod 755 /home/nifi/01-1.sh
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
* change file mode & clean up output directory
```
$ chmod 755 /home/nifi/02-1.py
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
* change file mode & clean up output directory
```
$ chmod 755 /home/nifi/03-1.py
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