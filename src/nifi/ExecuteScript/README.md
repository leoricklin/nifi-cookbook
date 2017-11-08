# Recipe: 01.Modify flow file content
## Use case: 

## Approach:

## Examples:
* change file mode & clean up output directory
'''
$ chmod 755 /home/nifi/01-1.sh
$ rm -f /home/nifi/output.log/*
'''
* execute nifi flow
* check the output
'''
$ cat /home/nifi/output.log/42190644392215
hello
world
i'm john
MSG=this is message
qazwsx
'''

# Recipe: 02.Parsing flow file content
## Use case: 

## Approach:

## Examples:
* change file mode & clean up output directory
'''
$ chmod 755 /home/nifi/02-1.py
$ rm -f /home/nifi/output.log/*
'''
* execute nifi flow
* check the output
'''
$ cat /home/nifi/output.log/65288338611032
insert into tab (key, value) values ('successRate (1000/1000)','100.00%');
insert into tab (key, value) values ('avgDuration','0:04:43');
insert into tab (key, value) values ('overwriteRate','89.70%');
'''